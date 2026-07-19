from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from models.execution_result import ExecutionResult
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)


class FakePositionExitExecutionService:
    """
    Simulates the already-tested PositionExitExecutionService boundary.

    The runner must call this service instead of the legacy ExitEngine.
    """

    def __init__(self) -> None:
        self.execute_calls = 0
        self.received_session = None
        self.received_decision = None

    def execute(
        self,
        *,
        session,
        decision,
    ):
        self.execute_calls += 1
        self.received_session = session
        self.received_decision = decision

        execution = ExecutionResult(
            accepted=True,
            status="FILLED",
            order=None,
            message="Filled by fake IBKR broker.",
            executed_price=93.50,
            executed_quantity=2,
            executed_at=datetime(
                2026,
                7,
                16,
                20,
                30,
                0,
            ),
        )

        # This is provisional ExecutionEngine state.
        provisional_portfolio = PaperPortfolio(
            cash=987.0,
            positions={},
        )

        engine_result = SimpleNamespace(
            execution=execution,
            portfolio=provisional_portfolio,
        )

        return SimpleNamespace(
            symbol="AAPL",
            action=decision.action,
            attempted=True,
            reason=decision.reason,
            execution_result=engine_result,
        )


class FakeTradingSessionSyncService:
    """
    Simulates authoritative broker truth after the SELL fill.
    """

    def __init__(self) -> None:
        self.synchronize_calls = 0
        self.received_session = None
        self.received_expected_quantities = None
        self.received_attempts = None
        self.received_retry_delay_seconds = None

    def synchronize(
        self,
        session,
        *,
        expected_position_quantities=None,
        attempts=1,
        retry_delay_seconds=0.25,
        expected_symbols=None,
    ):
        self.synchronize_calls += 1
        self.received_session = session
        self.received_expected_quantities = (
            expected_position_quantities
        )
        self.received_attempts = attempts
        self.received_retry_delay_seconds = (
            retry_delay_seconds
        )

        # Authoritative IBKR truth: position is fully closed.
        return TradingSession(
            name=session.name,
            portfolio=PaperPortfolio(
                cash=987.0,
                positions={},
            ),
            position_states={},
            risk_plans={},
            status=session.status,
        )


class FakeTradeJournalRepository:
    def __init__(self) -> None:
        self.entries = []

    def append(self, entry) -> None:
        self.entries.append(entry)


class FailingLegacyExitEngine:
    """
    The broker route must prevent the legacy ExitEngine from being used.
    """

    def execute(self, *args, **kwargs):
        raise AssertionError(
            "Legacy ExitEngine must not be called "
            "when broker exit execution is configured."
        )


class ClosedMarketSessionService:
    def is_symbol_market_open(self, symbol: str) -> bool:
        return False


def create_session() -> TradingSession:
    return TradingSession(
        name="Autonomous broker exit lifecycle test",
        portfolio=PaperPortfolio(
            cash=800.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=2,
                    entry_price=100.0,
                    current_price=94.0,
                    currency="USD",
                    fx_rate_to_base=0.9,
                ),
            },
        ),
        position_states={
            "AAPL": PositionState(
                symbol="AAPL",
                entry_price=100.0,
                current_stop_loss=95.0,
                highest_price=112.0,
                current_price=94.0,
                break_even_active=True,
                trailing_stop_active=True,
                target_1_hit=True,
                target_2_hit=False,
                target_3_hit=False,
            ),
        },
        risk_plans={
            "AAPL": RiskPlan(
                symbol="AAPL",
                entry_price=100.0,
                stop_loss=95.0,
                target_1=104.0,
                target_2=112.0,
                target_3=120.0,
                risk_percent=5.0,
                reward_percent=20.0,
                risk_reward_ratio=4.0,
                confidence=0.90,
                notes="Autonomous broker exit lifecycle test.",
            ),
        },
        status="ACTIVE",
    )


def test_runner_routes_exit_through_broker_execution_and_sync() -> None:
    exit_service = FakePositionExitExecutionService()
    sync_service = FakeTradingSessionSyncService()
    journal_repository = FakeTradeJournalRepository()

    runner = AutonomousPaperTradingRunner(
        position_exit_execution_service=exit_service,
        trading_session_sync_service=sync_service,
        trade_journal_repository=journal_repository,
        exit_engine=FailingLegacyExitEngine(),
    )

    original_session = create_session()

    result = runner._process_open_position_exits(
        session=original_session,
        cycle_number=7,
        session_id="SESSION-TEST-001",
    )

    # The existing PositionMonitor must identify the trailing-stop exit.
    assert exit_service.execute_calls == 1

    decision = exit_service.received_decision

    assert decision is not None
    assert decision.symbol == "AAPL"
    assert decision.action == "STOP_LOSS"
    assert decision.reason == "Dynamic trailing stop reached."

    # The runner must synchronize using expected broker quantity zero.
    assert sync_service.synchronize_calls == 1
    assert sync_service.received_expected_quantities == {
        "AAPL": 0,
    }
    assert sync_service.received_attempts == 8
    assert (
        sync_service.received_retry_delay_seconds
        == 0.25
    )

    # TradingSession must now reflect authoritative broker truth.
    assert result.portfolio.cash == 987.0
    assert "AAPL" not in result.portfolio.positions

    assert "AAPL" not in result.position_states
    assert "AAPL" not in result.risk_plans

    # Journal must be written after execution and synchronization.
    assert len(journal_repository.entries) == 1

    entry = journal_repository.entries[0]

    assert entry.symbol == "AAPL"
    assert entry.action == "CLOSE_POSITION"
    assert entry.decision == "STOP_LOSS"

    # Actual broker fill information, not the observed market price.
    assert entry.entry_price == 100.0
    assert entry.exit_price == 93.50
    assert entry.quantity == 2
    # Journal monetary totals use the EUR portfolio base currency while
    # entry/exit prices remain in the USD quote currency.
    assert entry.invested_amount == 180.0
    assert entry.realized_profit_loss == -11.7

    assert entry.timestamp == datetime(
        2026,
        7,
        16,
        20,
        30,
        0,
    )

    assert entry.recommendation_reason == (
        "Dynamic trailing stop reached."
    )
    assert entry.cycle_number == 7
    assert entry.session_id == "SESSION-TEST-001"


def test_runner_does_not_submit_sell_when_market_is_closed() -> None:
    exit_service = FakePositionExitExecutionService()

    runner = AutonomousPaperTradingRunner(
        position_exit_execution_service=exit_service,
        market_session_service=ClosedMarketSessionService(),
        exit_engine=FailingLegacyExitEngine(),
    )

    result = runner._process_open_position_exits(
        session=create_session(),
        cycle_number=1,
        session_id="SESSION-CLOSED-MARKET",
    )

    assert exit_service.execute_calls == 0
    assert "AAPL" in result.portfolio.positions
    assert "AAPL" in result.position_states
    assert "AAPL" in result.risk_plans


def test_runner_does_not_execute_or_sync_hold_decision() -> None:
    exit_service = FakePositionExitExecutionService()
    sync_service = FakeTradingSessionSyncService()
    journal_repository = FakeTradeJournalRepository()

    session = create_session()

    # Price is above stop and below final target.
    session.portfolio.positions["AAPL"] = PaperPosition(
        symbol="AAPL",
        quantity=2,
        entry_price=100.0,
        current_price=110.0,
    )
    session.position_states["AAPL"].current_price = 110.0
    session.position_states["AAPL"].current_stop_loss = 105.0

    runner = AutonomousPaperTradingRunner(
        position_exit_execution_service=exit_service,
        trading_session_sync_service=sync_service,
        trade_journal_repository=journal_repository,
        exit_engine=FailingLegacyExitEngine(),
    )

    result = runner._process_open_position_exits(
        session=session,
        cycle_number=8,
        session_id="SESSION-TEST-002",
    )

    assert exit_service.execute_calls == 0
    assert sync_service.synchronize_calls == 0
    assert journal_repository.entries == []

    assert "AAPL" in result.portfolio.positions
    assert "AAPL" in result.position_states
    assert "AAPL" in result.risk_plans


def run() -> None:
    tests = [
        test_runner_routes_exit_through_broker_execution_and_sync,
        test_runner_does_not_submit_sell_when_market_is_closed,
        test_runner_does_not_execute_or_sync_hold_decision,
    ]

    passed = 0

    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")

    print()
    print(
        "AUTONOMOUS BROKER EXIT LIFECYCLE TESTS: "
        f"{passed} passed"
    )


if __name__ == "__main__":
    run()
