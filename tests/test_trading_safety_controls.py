from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

from models.order import Order
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.trading_session import TradingSession
from models.position_state import PositionState
from services.earnings_calendar_service import EarningsCalendarService
from services.execution_quality_gate import ExecutionQualityGate, ExecutionQuote
from services.ibkr.ibkr_broker import IbkrBroker, IbkrOrderOutcome
from services.ibkr.ibkr_quote_provider import IbkrQuoteProvider
from services.net_expectancy_service import NetExpectancyService
from services.portfolio_concentration_gate import PortfolioConcentrationGate
from services.session_risk_circuit_breaker import SessionRiskCircuitBreaker
from services.autonomous_paper_trading_runner import AutonomousPaperTradingRunner
from services.ibkr.ibkr_order_transport import IbkrProtectiveExecution
from tests.test_completed_trade_records import (
    MemoryCompletedTrades,
    MemoryJournal,
    journal,
)


NOW = datetime(2026, 7, 19, 12, 0, tzinfo=UTC)


def test_execution_quality_gate_builds_bounded_buy_limit():
    decision = ExecutionQualityGate().evaluate(
        quote=ExecutionQuote(
            symbol="AAPL",
            bid=100.0,
            ask=100.10,
            received_at=NOW,
            bid_size=100,
            ask_size=100,
        ),
        side="BUY",
        max_spread_pct=0.002,
        max_quote_age_seconds=5.0,
        max_slippage_pct=0.001,
        now=NOW + timedelta(seconds=1),
    )
    assert decision.allowed is True
    assert decision.marketable_limit_price == 100.2001


def test_execution_quality_gate_rejects_wide_and_stale_quotes():
    gate = ExecutionQualityGate()
    wide = gate.evaluate(
        quote=ExecutionQuote("AAPL", 99.0, 101.0, NOW, 100, 100),
        side="BUY",
        max_spread_pct=0.003,
        max_quote_age_seconds=5.0,
        max_slippage_pct=0.001,
        now=NOW,
    )
    stale = gate.evaluate(
        quote=ExecutionQuote("AAPL", 100.0, 100.1, NOW, 100, 100),
        side="BUY",
        max_spread_pct=0.003,
        max_quote_age_seconds=5.0,
        max_slippage_pct=0.001,
        now=NOW + timedelta(seconds=6),
    )
    assert wide.allowed is False
    assert stale.allowed is False


class FakeIbkrQuoteClient:
    def __init__(self):
        import threading

        self.connection_ready = threading.Event()
        self.quote_ready = threading.Event()
        self.connected = False
        self.bid = None
        self.ask = None
        self.bid_size = 0.0
        self.ask_size = 0.0
        self.received_at = None
        self.errors = []

    def reset_quote_state(self):
        self.connection_ready.clear()
        self.quote_ready.clear()
        self.errors = []

    def connect(self, host, port, clientId):
        self.connected = True

    def run(self):
        self.connection_ready.set()

    def isConnected(self):
        return self.connected

    def reqMarketDataType(self, market_data_type):
        assert market_data_type == 1

    def reqMktData(self, *args):
        self.bid = 100.0
        self.ask = 100.1
        self.bid_size = 10
        self.ask_size = 12
        self.received_at = datetime.now(UTC)
        self.quote_ready.set()

    def cancelMktData(self, request_id):
        pass

    def disconnect(self):
        self.connected = False


def test_ibkr_quote_provider_returns_live_top_of_book():
    quote = IbkrQuoteProvider(
        timeout_seconds=0.1,
        client=FakeIbkrQuoteClient(),
    ).get_quote("AAPL")
    assert quote.bid == 100.0
    assert quote.ask == 100.1
    assert quote.bid_size == 10


class FakeQuoteProvider:
    def get_quote(self, symbol):
        return ExecutionQuote(
            symbol,
            100.0,
            100.1,
            datetime.now(UTC),
            100,
            100,
        )


class FakeBracketTransport:
    def __init__(self):
        self.bracket = None

    def submit_bracket_order(self, **kwargs):
        self.bracket = kwargs
        return IbkrOrderOutcome(
            status="FILLED",
            filled_quantity=2,
            average_fill_price=100.1,
            child_order_ids=(502, 503),
        )

    def submit_order(self, **kwargs):
        raise AssertionError("Protected BUY must use bracket submission.")


def test_ibkr_protected_buy_uses_limit_parent_and_two_children():
    transport = FakeBracketTransport()
    broker = IbkrBroker(
        transport=transport,
        enable_native_protective_orders=True,
        quote_provider=FakeQuoteProvider(),
    )
    result = broker.execute(
        Order(
            symbol="AAPL",
            side="BUY",
            quantity=2,
            order_type="MARKET",
            price=100.0,
            created_at=NOW,
            stop_loss_price=96.0,
            take_profit_price=108.0,
            client_order_id="trade-1",
            oca_group="ORION-trade-1",
        )
    )
    assert result.accepted is True
    bracket = transport.bracket
    assert bracket["parent_order"].orderType == "LMT"
    assert bracket["parent_order"].transmit is False
    assert bracket["take_profit_order"].orderType == "LMT"
    assert bracket["take_profit_order"].lmtPrice == 108.0
    assert bracket["take_profit_order"].ocaGroup == "ORION-trade-1"
    assert bracket["stop_loss_order"].orderType == "STP"
    assert bracket["stop_loss_order"].auxPrice == 96.0
    assert bracket["stop_loss_order"].transmit is True
    assert bracket["stop_loss_order"].ocaGroup == "ORION-trade-1"


def _session(*positions):
    mapped = {position.symbol: position for position in positions}
    return TradingSession(
        name="test",
        portfolio=PaperPortfolio(cash=1000.0, positions=mapped),
    )


def _record(net, closed_at):
    return SimpleNamespace(
        estimated_net_profit_loss=net,
        closed_at=closed_at,
    )


def test_session_circuit_breaker_blocks_daily_loss_and_loss_streak():
    breaker = SessionRiskCircuitBreaker()
    daily = breaker.evaluate(
        session=_session(
            PaperPosition("AAPL", 1, 100.0, 75.0),
        ),
        completed_trades=[],
        max_daily_loss_pct=0.02,
        max_consecutive_losses=3,
        cooldown_minutes=60,
        now=NOW,
    )
    streak = breaker.evaluate(
        session=_session(),
        completed_trades=[
            _record(-1.0, NOW - timedelta(minutes=3)),
            _record(-1.0, NOW - timedelta(minutes=2)),
            _record(-1.0, NOW - timedelta(minutes=1)),
        ],
        max_daily_loss_pct=0.5,
        max_consecutive_losses=3,
        cooldown_minutes=60,
        now=NOW,
    )
    assert daily.entries_allowed is False
    assert streak.entries_allowed is False


def test_session_circuit_breaker_blocks_repeated_broker_failures():
    decision = SessionRiskCircuitBreaker().evaluate(
        session=_session(),
        completed_trades=[],
        max_daily_loss_pct=0.5,
        max_consecutive_losses=3,
        cooldown_minutes=60,
        consecutive_order_failures=3,
        max_consecutive_order_failures=3,
        now=NOW,
    )
    assert decision.entries_allowed is False
    assert "broker" in decision.reason.lower()


def test_concentration_gate_uses_market_sector_and_cluster(tmp_path):
    metadata = tmp_path / "metadata.csv"
    metadata.write_text(
        "symbol,sector,correlation_cluster\n"
        "AAPL,TECH,US_GROWTH\nMSFT,TECH,US_GROWTH\n",
        encoding="utf-8",
    )
    session = _session(PaperPosition("AAPL", 2, 100.0, 100.0))
    decision = PortfolioConcentrationGate(metadata).evaluate(
        session=session,
        symbol="MSFT",
        proposed_value=200.0,
        max_positions_per_market=10,
        max_market_exposure_pct=0.9,
        max_positions_per_sector=1,
        max_sector_exposure_pct=0.9,
        max_positions_per_correlation_cluster=5,
    )
    assert decision.allowed is False
    assert "sector" in decision.reason.lower()


def test_instrument_metadata_covers_the_complete_ibkr_universe():
    root = Path(__file__).resolve().parents[1]
    symbols = {
        line.strip().upper()
        for line in (
            root / "data/universes/ibkr_eu_us_validation.csv"
        ).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    metadata = PortfolioConcentrationGate(
        root / "data/instrument_metadata.csv"
    )._load()
    assert set(metadata) == symbols


def test_known_earnings_date_blocks_entry(tmp_path):
    calendar = tmp_path / "earnings.csv"
    calendar.write_text(
        "symbol,earnings_date\nAAPL,2026-07-20\n",
        encoding="utf-8",
    )
    decision = EarningsCalendarService(calendar).evaluate(
        symbol="AAPL",
        evaluated_on=NOW.date(),
        blackout_days=1,
    )
    assert decision.allowed is False
    assert decision.data_available is True


def test_net_expectancy_is_offline_and_cost_aware():
    result = NetExpectancyService().analyze(
        [_record(5.0, NOW), _record(-3.0, NOW), _record(4.0, NOW)],
        minimum_sample_size=3,
    )
    assert result.sample_size == 3
    assert result.net_expectancy_per_trade == 2.0
    assert result.total_net_profit_loss == 6.0
    assert result.sufficient_sample is True


class FakeProtectiveReconciler:
    def find_protective_exit(self, **kwargs):
        return IbkrProtectiveExecution(
            symbol="AAPL",
            order_reference="trade-1:SL",
            side="SLD",
            quantity=2,
            price=96.0,
            executed_at=NOW,
            order_id=502,
        )


def test_native_protective_fill_is_journaled_with_original_trade_id():
    trade_journal = MemoryJournal(
        [journal(action="OPEN_POSITION", timestamp=NOW)]
    )
    completed = MemoryCompletedTrades()
    runner = AutonomousPaperTradingRunner(
        trade_journal_repository=trade_journal,
        completed_trade_repository=completed,
        protective_execution_reconciler=FakeProtectiveReconciler(),
    )
    position = PaperPosition("AAPL", 2, 100.0, 100.0)
    state = PositionState(
        symbol="AAPL",
        trade_id="trade-1",
        entry_price=100.0,
        current_stop_loss=96.0,
        highest_price=100.0,
        current_price=100.0,
    )
    runner._reconcile_native_protective_exits(
        positions_before={"AAPL": position},
        states_before={"AAPL": state},
        synchronized_session=_session(),
        cycle_number=2,
        session_id="session-1",
    )
    assert trade_journal.entries[-1].decision == "STOP_LOSS"
    assert trade_journal.entries[-1].trade_id == "trade-1"
    assert completed.records[0].exit_reason.startswith("Confirmed IBKR")


class FakeOpenJournalBuilder:
    def build_open_trade_entry(self, **kwargs):
        return journal(
            action="OPEN_POSITION",
            timestamp=NOW,
            trade_id="",
        )


def test_open_journal_persists_generated_trade_id_before_append():
    repository = MemoryJournal([])
    runner = AutonomousPaperTradingRunner(
        trade_journal_repository=repository,
        trade_journal_builder=FakeOpenJournalBuilder(),
    )
    position = PaperPosition("AAPL", 2, 100.0, 100.0)
    session = _session(position)
    session.position_states["AAPL"] = PositionState(
        symbol="AAPL",
        trade_id="generated-trade-id",
        entry_price=100.0,
        current_stop_loss=96.0,
        highest_price=100.0,
        current_price=100.0,
    )
    runner._append_open_trade_journal_entry(
        decision=SimpleNamespace(symbol="AAPL"),
        session=session,
        cycle_number=1,
        session_id="session-1",
    )
    assert repository.entries[0].trade_id == "generated-trade-id"
