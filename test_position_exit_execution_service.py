from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from models.trading_session import TradingSession
from services.position_exit_execution_service import (
    PositionExitExecutionService,
)
from services.position_monitor import PositionMonitorResult


@dataclass(frozen=True)
class FakeExecutionEngineResult:
    marker: str = "EXECUTED"


class FakeExecutionEngine:
    def __init__(self) -> None:
        self.execute_called = False
        self.received_context = None
        self.result = FakeExecutionEngineResult()

    def execute(self, context):
        self.execute_called = True
        self.received_context = context
        return self.result


def create_risk_plan() -> RiskPlan:
    return RiskPlan(
        symbol="AAPL",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=105.0,
        target_2=110.0,
        target_3=115.0,
        risk_percent=5.0,
        reward_percent=15.0,
        risk_reward_ratio=3.0,
        confidence=0.90,
        notes="Position exit execution test",
    )


def create_session() -> TradingSession:
    return TradingSession(
        name="Position exit execution test",
        portfolio=PaperPortfolio(
            cash=800.0,
            positions={
                "AAPL": PaperPosition(
                    symbol="AAPL",
                    quantity=2,
                    entry_price=100.0,
                    current_price=110.0,
                ),
            },
        ),
        position_states={
            "AAPL": PositionState(
                symbol="AAPL",
                entry_price=100.0,
                current_stop_loss=105.0,
                highest_price=112.0,
                current_price=110.0,
                opened_at=datetime(
                    2026,
                    7,
                    16,
                    12,
                    0,
                    0,
                ),
            ),
        },
        risk_plans={
            "AAPL": create_risk_plan(),
        },
    )


def create_exit_decision(
    *,
    action: str = "STOP_LOSS",
) -> PositionMonitorResult:
    return PositionMonitorResult(
        symbol="AAPL",
        action=action,
        reason="Dynamic trailing stop reached.",
        current_price=110.0,
        entry_price=100.0,
        unrealized_profit_loss=20.0,
        unrealized_return_percent=0.10,
    )


def test_converts_exit_decision_to_close_position_request() -> None:
    execution_engine = FakeExecutionEngine()

    service = PositionExitExecutionService(
        execution_engine=execution_engine,
    )

    session = create_session()
    decision = create_exit_decision()

    result = service.execute(
        session=session,
        decision=decision,
    )

    assert result.attempted is True
    assert result.symbol == "AAPL"
    assert result.action == "STOP_LOSS"
    assert result.reason == "Dynamic trailing stop reached."
    assert result.execution_result is execution_engine.result

    assert execution_engine.execute_called is True

    context = execution_engine.received_context

    assert context is not None
    assert context.portfolio is session.portfolio
    assert context.trading_mode == "PAPER"

    request = context.request

    assert request.symbol == "AAPL"
    assert request.action == "CLOSE_POSITION"
    assert request.entry_price == 110.0
    assert request.quantity == 2
    assert request.risk_plan is session.risk_plans["AAPL"]
    assert request.confidence == 1.0
    assert request.strategy == "POSITION_LIFECYCLE"
    assert request.source == "PositionMonitor"


def test_hold_does_not_call_execution_engine() -> None:
    execution_engine = FakeExecutionEngine()

    service = PositionExitExecutionService(
        execution_engine=execution_engine,
    )

    result = service.execute(
        session=create_session(),
        decision=create_exit_decision(
            action="HOLD",
        ),
    )

    assert result.attempted is False
    assert result.action == "HOLD"
    assert result.execution_result is None

    assert execution_engine.execute_called is False
    assert execution_engine.received_context is None


def test_rejects_exit_when_position_does_not_exist() -> None:
    execution_engine = FakeExecutionEngine()

    service = PositionExitExecutionService(
        execution_engine=execution_engine,
    )

    session = create_session()
    session.portfolio.positions.clear()

    try:
        service.execute(
            session=session,
            decision=create_exit_decision(),
        )
    except ValueError as exc:
        assert "open position does not exist" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for missing position."
        )

    assert execution_engine.execute_called is False


def test_rejects_exit_when_risk_plan_does_not_exist() -> None:
    execution_engine = FakeExecutionEngine()

    service = PositionExitExecutionService(
        execution_engine=execution_engine,
    )

    session = create_session()
    session.risk_plans.clear()

    try:
        service.execute(
            session=session,
            decision=create_exit_decision(),
        )
    except ValueError as exc:
        assert "RiskPlan does not exist" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for missing RiskPlan."
        )

    assert execution_engine.execute_called is False


def test_rejects_unknown_exit_action() -> None:
    execution_engine = FakeExecutionEngine()

    service = PositionExitExecutionService(
        execution_engine=execution_engine,
    )

    try:
        service.execute(
            session=create_session(),
            decision=create_exit_decision(
                action="UNKNOWN_EXIT",
            ),
        )
    except ValueError as exc:
        assert "Unsupported position exit action" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for unknown exit action."
        )

    assert execution_engine.execute_called is False


def run() -> None:
    tests = [
        test_converts_exit_decision_to_close_position_request,
        test_hold_does_not_call_execution_engine,
        test_rejects_exit_when_position_does_not_exist,
        test_rejects_exit_when_risk_plan_does_not_exist,
        test_rejects_unknown_exit_action,
    ]

    passed = 0

    for test in tests:
        test()
        passed += 1
        print(f"PASS: {test.__name__}")

    print()
    print(
        "POSITION EXIT EXECUTION SERVICE TESTS: "
        f"{passed} passed"
    )


if __name__ == "__main__":
    run()