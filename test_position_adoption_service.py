from __future__ import annotations

from datetime import UTC, datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_adoption import PositionAdoptionConfig
from models.trading_session import TradingSession
from services.position_adoption_service import PositionAdoptionService
from services.position_monitor import PositionMonitor
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from test_autonomous_broker_exit_lifecycle import (
    FakePositionExitExecutionService,
    FakeTradeJournalRepository,
)


def create_session() -> TradingSession:
    return TradingSession(
        name="IBKR adoption test",
        portfolio=PaperPortfolio(
            cash=7000.0,
            base_currency="EUR",
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=2,
                    entry_price=100.0,
                    current_price=94.0,
                    currency="USD",
                    fx_rate_to_base=0.90,
                ),
                "ASML.AS": PaperPosition(
                    symbol="ASML.AS",
                    quantity=1,
                    entry_price=1200.0,
                    current_price=1210.0,
                    currency="EUR",
                ),
            },
        ),
    )


def test_explicit_positions_are_adopted_with_orion_exit_plan() -> None:
    adopted_at = datetime(2026, 7, 17, 9, 0, tzinfo=UTC)
    service = PositionAdoptionService(
        PositionAdoptionConfig(
            allowed_symbols=("AAPL", "ASML.AS"),
        )
    )

    result = service.adopt(
        session=create_session(),
        trading_config=LivePaperTradingConfig(),
        adopted_at=adopted_at,
    )

    assert {record.symbol for record in result.records} == {
        "AAPL",
        "ASML.AS",
    }
    assert set(result.session.position_states) == {"AAPL", "ASML.AS"}
    assert set(result.session.risk_plans) == {"AAPL", "ASML.AS"}
    assert result.session.risk_plans["AAPL"].stop_loss == 96.0
    assert result.session.risk_plans["AAPL"].target_3 == 108.0
    assert result.session.position_states["AAPL"].opened_at == adopted_at
    assert "Original BUY rationale unavailable" in (
        result.session.risk_plans["AAPL"].notes
    )


def test_adopted_position_uses_existing_managed_sell_strategy() -> None:
    service = PositionAdoptionService(
        PositionAdoptionConfig(allowed_symbols=("AAPL",))
    )
    result = service.adopt(
        session=create_session(),
        trading_config=LivePaperTradingConfig(),
    )

    decision = PositionMonitor().evaluate_managed(
        position=result.session.portfolio.positions["AAPL"],
        state=result.session.position_states["AAPL"],
        risk_plan=result.session.risk_plans["AAPL"],
        config=LivePaperTradingConfig(),
    )

    assert decision.action == "STOP_LOSS"
    assert decision.reason == "Initial lifecycle stop reached."


def test_unlisted_position_remains_unmanaged() -> None:
    service = PositionAdoptionService(
        PositionAdoptionConfig(allowed_symbols=("AAPL",))
    )
    result = service.adopt(
        session=create_session(),
        trading_config=LivePaperTradingConfig(),
    )

    assert "ASML.AS" not in result.session.position_states
    assert "ASML.AS" not in result.session.risk_plans


def test_adoption_is_idempotent() -> None:
    service = PositionAdoptionService(
        PositionAdoptionConfig(allowed_symbols=("AAPL",))
    )
    first = service.adopt(
        session=create_session(),
        trading_config=LivePaperTradingConfig(),
    )
    second = service.adopt(
        session=first.session,
        trading_config=LivePaperTradingConfig(),
    )

    assert second.records == ()


def test_adopted_stop_routes_to_canonical_sell_service() -> None:
    adoption_service = PositionAdoptionService(
        PositionAdoptionConfig(allowed_symbols=("AAPL",))
    )
    adoption = adoption_service.adopt(
        session=create_session(),
        trading_config=LivePaperTradingConfig(),
    )
    exit_service = FakePositionExitExecutionService()
    runner = AutonomousPaperTradingRunner(
        position_exit_execution_service=exit_service,
    )

    runner._process_open_position_exits(
        session=adoption.session,
        cycle_number=1,
        session_id="ADOPTION-SELL-TEST",
    )

    assert exit_service.execute_calls == 1
    assert exit_service.received_decision.symbol == "AAPL"
    assert exit_service.received_decision.action == "STOP_LOSS"


def test_adoption_reason_is_written_to_trade_journal() -> None:
    service = PositionAdoptionService(
        PositionAdoptionConfig(allowed_symbols=("AAPL",))
    )
    adoption = service.adopt(
        session=create_session(),
        trading_config=LivePaperTradingConfig(),
    )
    journal = FakeTradeJournalRepository()
    runner = AutonomousPaperTradingRunner(
        trade_journal_repository=journal,
    )

    runner._append_adoption_journal_entries(
        records=adoption.records,
        session=adoption.session,
        cycle_number=1,
        session_id="ADOPTION-JOURNAL-TEST",
    )

    assert len(journal.entries) == 1
    entry = journal.entries[0]
    assert entry.action == "ADOPT_POSITION"
    assert entry.decision == "ADOPT"
    assert "original BUY rationale is unavailable" in (
        entry.recommendation_reason
    )
    assert entry.session_id == "ADOPTION-JOURNAL-TEST"
