from __future__ import annotations

from models.position_state import PositionState
from models.risk_plan import RiskPlan


class PositionStateFactory:
    """
    Creates the initial runtime state for an open position.
    """

    def create(
        self,
        risk_plan: RiskPlan,
    ) -> PositionState:

        return PositionState(
            symbol=risk_plan.symbol,
            entry_price=risk_plan.entry_price,
            current_stop_loss=risk_plan.stop_loss,
            highest_price=risk_plan.entry_price,
            current_price=risk_plan.entry_price,
        )