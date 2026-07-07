from __future__ import annotations

from dataclasses import dataclass

from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.position_manager import (
    PositionManager,
    PositionManagementResult,
)


@dataclass(frozen=True)
class PositionUpdateResult:
    """
    Result of updating an open position.

    This object is deterministic and contains the updated
    runtime state after processing one market update.
    """

    state: PositionState

    management: PositionManagementResult


class PositionUpdateEngine:
    """
    Coordinates deterministic updates of an open position.

    Responsibilities
    ----------------
    - Update runtime position state
    - Coordinate PositionManager
    - Produce updated PositionState

    Does NOT
    --------
    - Execute trades
    - Generate BUY/HOLD/SELL
    - Persist state
    """

    def __init__(
        self,
        position_manager: PositionManager | None = None,
    ):
        self.position_manager = (
            position_manager
            or PositionManager()
        )

    def update(
        self,
        state: PositionState,
        risk_plan: RiskPlan,
        current_price: float,
    ) -> PositionUpdateResult:

        management = self.position_manager.manage(
            symbol=state.symbol,
            risk_plan=risk_plan,
            current_price=current_price,
        )

        updated_state = PositionState(
            symbol=state.symbol,
            entry_price=state.entry_price,
            current_stop_loss=management.stop_loss,
            highest_price=max(
                state.highest_price,
                current_price,
            ),
            current_price=current_price,
            break_even_active=management.break_even.activated
            or state.break_even_active,
            trailing_stop_active=state.trailing_stop_active,
            target_1_hit=state.target_1_hit
            or current_price >= risk_plan.target_1,
            target_2_hit=state.target_2_hit
            or current_price >= risk_plan.target_2,
            target_3_hit=state.target_3_hit
            or current_price >= risk_plan.target_3,
        )

        return PositionUpdateResult(
            state=updated_state,
            management=management,
        )