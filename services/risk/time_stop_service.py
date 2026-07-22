from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from models.position_state import PositionState


@dataclass(frozen=True)
class TimeStopResult:
    """
    Result of deterministic time-stop evaluation.

    The day-based fields remain available for compatibility
    with existing summaries and tests.

    The hour-based fields support exact 24/48-hour evaluation.
    """

    activated: bool

    days_open: int

    maximum_days: int

    reason: str

    elapsed_hours: float = 0.0

    maximum_hours: float = 0.0


class TimeStopService:
    """
    Evaluates whether a managed position has reached
    its configured maximum holding period.

    Uses elapsed clock time so maximum_days=2
    represents exactly 48 elapsed hours.

    No trade execution.
    No AI.
    No persistence.
    """

    def evaluate(
        self,
        state: PositionState,
        maximum_days: int,
        now: datetime | None = None,
        maximum_minutes: int | None = None,
    ) -> TimeStopResult:
        if maximum_days < 1:
            raise ValueError(
                "maximum_days must be at least 1."
            )
        if maximum_minutes is not None and maximum_minutes < 1:
            raise ValueError(
                "maximum_minutes must be at least 1 when set."
            )

        opened_at = self._as_utc(state.opened_at)
        evaluated_at = self._as_utc(
            now or datetime.now(UTC)
        )

        elapsed_seconds = max(
            0.0,
            (evaluated_at - opened_at).total_seconds(),
        )
        elapsed_hours = elapsed_seconds / 3600.0
        maximum_hours = (
            float(maximum_minutes) / 60.0
            if maximum_minutes is not None
            else float(maximum_days * 24)
        )
        days_open = int(elapsed_hours // 24)

        if elapsed_hours < maximum_hours:
            return TimeStopResult(
                activated=False,
                days_open=days_open,
                maximum_days=maximum_days,
                reason="Holding period still valid.",
                elapsed_hours=round(elapsed_hours, 3),
                maximum_hours=maximum_hours,
            )

        return TimeStopResult(
            activated=True,
            days_open=days_open,
            maximum_days=maximum_days,
            reason=(
                "Maximum intraday holding period reached."
                if maximum_minutes is not None
                else "Maximum holding period reached."
            ),
            elapsed_hours=round(elapsed_hours, 3),
            maximum_hours=maximum_hours,
        )

    def _as_utc(
        self,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)

        return value.astimezone(UTC)
