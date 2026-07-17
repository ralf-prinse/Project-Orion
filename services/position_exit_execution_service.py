from __future__ import annotations

from dataclasses import dataclass

from models.execution_context import ExecutionContext
from models.execution_request import ExecutionRequest
from models.trading_session import TradingSession
from services.execution_engine import (
    ExecutionEngine,
    ExecutionEngineResult,
)
from services.position_monitor import PositionMonitorResult


@dataclass(frozen=True)
class PositionExitExecutionResult:
    """
    Result of translating an existing exit decision into execution.

    attempted:
        True when a CLOSE_POSITION request was sent to ExecutionEngine.

    execution_result:
        The complete ExecutionEngine result when execution was attempted.
        None for HOLD decisions.
    """

    symbol: str
    action: str
    attempted: bool
    reason: str
    execution_result: ExecutionEngineResult | None = None


class PositionExitExecutionService:
    """
    Connects deterministic position-exit decisions to ExecutionEngine.

    Responsibilities:

    - ignore HOLD decisions;
    - validate that the open position still exists;
    - load the existing RiskPlan from TradingSession;
    - create a broker-neutral CLOSE_POSITION request;
    - execute the request through ExecutionEngine.

    This service does not:

    - decide when to exit;
    - construct IBKR-specific orders;
    - synchronize broker truth;
    - write journals;
    - persist TradingSession;
    - mutate lifecycle state manually.
    """

    EXIT_ACTIONS = {
        "STOP_LOSS",
        "TAKE_PROFIT",
        "MAX_HOLDING_TIME",
    }

    def __init__(
        self,
        *,
        execution_engine: ExecutionEngine,
    ) -> None:
        self.execution_engine = execution_engine

    def execute(
        self,
        *,
        session: TradingSession,
        decision: PositionMonitorResult,
    ) -> PositionExitExecutionResult:
        symbol = decision.symbol.strip().upper()
        action = decision.action.strip().upper()

        if action == "HOLD":
            return PositionExitExecutionResult(
                symbol=symbol,
                action=action,
                attempted=False,
                reason="No exit execution required.",
            )

        if action not in self.EXIT_ACTIONS:
            raise ValueError(
                "Unsupported position exit action: "
                f"{decision.action!r}."
            )

        position = session.portfolio.positions.get(symbol)

        if position is None:
            raise ValueError(
                f"Cannot execute exit for {symbol}: "
                "open position does not exist."
            )

        risk_plan = session.risk_plans.get(symbol)

        if risk_plan is None:
            raise ValueError(
                f"Cannot execute managed exit for {symbol}: "
                "RiskPlan does not exist."
            )

        request = ExecutionRequest(
            symbol=symbol,
            action="CLOSE_POSITION",
            entry_price=decision.current_price,
            quantity=position.quantity,
            risk_plan=risk_plan,
            confidence=1.0,
            strategy="POSITION_LIFECYCLE",
            source="PositionMonitor",
        )

        context = ExecutionContext(
            request=request,
            portfolio=session.portfolio,
            trading_mode="PAPER",
            max_position_percentage=1.0,
            allow_fractional_shares=False,
        )

        execution_result = self.execution_engine.execute(
            context
        )

        return PositionExitExecutionResult(
            symbol=symbol,
            action=action,
            attempted=True,
            reason=decision.reason,
            execution_result=execution_result,
        )