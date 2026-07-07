from __future__ import annotations

from services.risk.break_even_service import BreakEvenResult
from services.risk.position_health_service import PositionHealthResult
from services.risk.time_stop_service import TimeStopResult
from services.risk.trailing_stop_service import TrailingStopResult
from models.position_management_summary import PositionManagementSummary


class PositionManagementSummaryBuilder:
    """
    Builds a central PositionManagementSummary from deterministic
    position-management service results.

    No trading decisions.
    No order execution.
    No persistence.
    No AI.
    """

    def build(
        self,
        symbol: str,
        current_price: float,
        stop_loss: float,
        break_even: BreakEvenResult,
        trailing_stop: TrailingStopResult,
        time_stop: TimeStopResult,
        position_health: PositionHealthResult,
    ) -> PositionManagementSummary:

        actions: list[str] = []
        warnings: list[str] = []

        if break_even.activated:
            actions.append("MOVE_STOP_TO_BREAK_EVEN")

        if trailing_stop.activated:
            actions.append("UPDATE_TRAILING_STOP")

        if time_stop.activated:
            actions.append("TIME_STOP_ACTIVE")
            warnings.append(time_stop.reason)

        warnings.extend(position_health.warnings)

        return PositionManagementSummary(
            symbol=str(symbol).strip().upper(),
            current_price=float(current_price),
            stop_loss=round(float(stop_loss), 2),
            status=position_health.status,
            score=position_health.score,
            actions=actions,
            warnings=warnings,
            break_even=break_even,
            trailing_stop=trailing_stop,
            time_stop=time_stop,
            position_health=position_health,
        )