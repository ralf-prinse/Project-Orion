from __future__ import annotations

from dataclasses import dataclass

from models.position_state import PositionState


@dataclass(frozen=True)
class TrailingStopResult:
    """
    Result of deterministic trailing-stop evaluation.
    """

    activated: bool
    new_stop_loss: float
    highest_price: float
    reason: str


class TrailingStopService:
    """
    Maintains a trailing stop for an open position.

    Rules
    -----
    - Stop-loss may only move upwards.
    - Highest price may only increase.
    - Never lowers protection.
    """

    DEFAULT_TRAIL_PERCENT = 0.05

    def evaluate(
        self,
        state: PositionState,
        current_price: float,
    ) -> TrailingStopResult:

        highest_price = max(
            state.highest_price,
            current_price,
        )

        candidate_stop = highest_price * (
            1 - self.DEFAULT_TRAIL_PERCENT
        )

        new_stop = max(
            state.current_stop_loss,
            candidate_stop,
        )

        activated = new_stop > state.current_stop_loss

        return TrailingStopResult(
            activated=activated,
            new_stop_loss=round(new_stop, 2),
            highest_price=round(highest_price, 2),
            reason=(
                "Trailing stop updated."
                if activated
                else "No trailing update."
            ),
        )