from __future__ import annotations

from dataclasses import dataclass

from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.risk.break_even_service import (
    BreakEvenResult,
    BreakEvenService,
)
from services.risk.trailing_stop_service import (
    TrailingStopResult,
    TrailingStopService,
)


@dataclass(frozen=True)
class PositionManagementResult:
    """
    Deterministic result of open-position management.

    No order execution.
    No persistence.
    No AI.
    """

    symbol: str
    current_price: float
    stop_loss: float

    break_even: BreakEvenResult
    trailing_stop: TrailingStopResult

    actions: list[str]


class PositionManager:
    """
    Coordinates deterministic management of an open position.

    Responsibilities
    ----------------
    - Coordinate BreakEvenService
    - Coordinate TrailingStopService
    - Produce a unified management result

    Does NOT
    --------
    - Execute trades
    - Generate BUY/HOLD/SELL
    - Persist state
    """

    def __init__(
        self,
        break_even_service: BreakEvenService | None = None,
        trailing_stop_service: TrailingStopService | None = None,
    ):
        self.break_even_service = (
            break_even_service
            or BreakEvenService()
        )

        self.trailing_stop_service = (
            trailing_stop_service
            or TrailingStopService()
        )

    def manage(
        self,
        state: PositionState,
        risk_plan: RiskPlan,
        current_price: float,
    ) -> PositionManagementResult:

        break_even = self.break_even_service.evaluate(
            risk_plan=risk_plan,
            current_price=current_price,
        )

        trailing = self.trailing_stop_service.evaluate(
            state=state,
            current_price=current_price,
        )

        new_stop = max(
            break_even.new_stop_loss,
            trailing.new_stop_loss,
        )

        actions: list[str] = []

        if break_even.activated:
            actions.append(
                "MOVE_STOP_TO_BREAK_EVEN"
            )

        if trailing.activated:
            actions.append(
                "UPDATE_TRAILING_STOP"
            )

        return PositionManagementResult(
            symbol=state.symbol,
            current_price=float(current_price),
            stop_loss=round(new_stop, 2),
            break_even=break_even,
            trailing_stop=trailing,
            actions=actions,
        )