from __future__ import annotations

from dataclasses import dataclass

from models.risk_plan import RiskPlan
from services.risk.break_even_service import (
    BreakEvenResult,
    BreakEvenService,
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
    actions: list[str]


class PositionManager:
    """
    Central manager for open-position risk management.

    Responsibilities
    ----------------
    - Coordinate position-management services
    - Apply break-even logic
    - Prepare future trailing-stop and position-health logic

    Does NOT
    --------
    - Generate BUY/HOLD/SELL decisions
    - Execute trades
    - Persist trades
    - Render UI
    """

    def __init__(
        self,
        break_even_service: BreakEvenService | None = None,
    ):
        self.break_even_service = break_even_service or BreakEvenService()

    def manage(
        self,
        symbol: str,
        risk_plan: RiskPlan,
        current_price: float,
    ) -> PositionManagementResult:

        break_even = self.break_even_service.evaluate(
            risk_plan=risk_plan,
            current_price=current_price,
        )

        actions: list[str] = []

        if break_even.activated:
            actions.append("MOVE_STOP_TO_BREAK_EVEN")

        return PositionManagementResult(
            symbol=str(symbol).strip().upper(),
            current_price=float(current_price),
            stop_loss=break_even.new_stop_loss,
            break_even=break_even,
            actions=actions,
        )