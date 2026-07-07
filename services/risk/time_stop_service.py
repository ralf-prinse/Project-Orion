from __future__ import annotations

from dataclasses import dataclass

from models.position_state import PositionState


@dataclass(frozen=True)
class TimeStopResult:
    """
    Result of deterministic time-stop evaluation.
    """

    activated: bool
    days_open: int
    maximum_days: int
    reason: str


class TimeStopService:
    """
    Evaluates whether an open position has exceeded
    its maximum holding period.

    No trade execution.

    No AI.

    No persistence.
    """

    DEFAULT_MAX_DAYS = 10

    def evaluate(
        self,
        state: PositionState,
        days_open: int,
    ) -> TimeStopResult:

        if days_open < self.DEFAULT_MAX_DAYS:

            return TimeStopResult(
                activated=False,
                days_open=days_open,
                maximum_days=self.DEFAULT_MAX_DAYS,
                reason="Holding period still valid.",
            )

        return TimeStopResult(
            activated=True,
            days_open=days_open,
            maximum_days=self.DEFAULT_MAX_DAYS,
            reason="Maximum holding period exceeded.",
        )