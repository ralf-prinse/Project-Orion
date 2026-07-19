from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.runtime_event import RuntimeEvent
from models.runtime_health import RuntimeHealth
from services.stores.repositories.runtime_event_repository import (
    RuntimeEventRepository,
)


class RuntimeSupervisor:
    """
    Observes the continuous runtime and records operational health.

    The supervisor never mutates TradingSession and never decides,
    sizes, opens, updates or closes trades.

    It is an operational observer only.
    """

    def __init__(
        self,
        event_repository: RuntimeEventRepository | None = None,
        clock: Callable[[], datetime] | None = None,
    ):
        self.event_repository = event_repository
        self.clock = clock or datetime.now
        self.health = RuntimeHealth()

    def runtime_started(self) -> None:
        now = self.clock()

        self.health.status = "RUNNING"
        self.health.started_at = now
        self.health.stopped_at = None
        self.health.last_heartbeat_at = now
        self.health.last_error = None

        self._record(
            "RUNTIME_STARTED",
            "Continuous runtime started.",
        )

    def iteration_started(
        self,
        iteration: int,
    ) -> None:
        now = self.clock()

        self.health.status = "RUNNING"
        self.health.current_iteration = iteration
        self.health.last_heartbeat_at = now

        self._record(
            "ITERATION_STARTED",
            f"Continuous iteration {iteration} started.",
            iteration=iteration,
        )

    def iteration_completed(
        self,
        iteration: int,
        result: AutonomousPaperTradingResult,
        duration_seconds: float,
    ) -> None:
        self._update_session_counts(result)

        self.health.status = "RUNNING"
        self.health.iterations_completed += 1
        self.health.last_iteration_duration_seconds = (
            duration_seconds
        )
        self.health.last_heartbeat_at = self.clock()
        self.health.last_error = None

        self._record(
            "ITERATION_COMPLETED",
            f"Continuous iteration {iteration} completed.",
            iteration=iteration,
            duration_seconds=duration_seconds,
        )

    def iteration_failed(
        self,
        iteration: int,
        duration_seconds: float,
        result: AutonomousPaperTradingResult | None = None,
        error: Exception | None = None,
    ) -> None:
        if result is not None:
            self._update_session_counts(result)

        self.health.status = "DEGRADED"
        self.health.failed_iterations += 1
        self.health.last_iteration_duration_seconds = (
            duration_seconds
        )
        self.health.last_heartbeat_at = self.clock()
        self.health.last_error = (
            repr(error)
            if error is not None
            else None
        )

        self._record(
            "ITERATION_FAILED",
            f"Continuous iteration {iteration} failed.",
            iteration=iteration,
            duration_seconds=duration_seconds,
            error=self.health.last_error,
        )

    def market_idle(
        self,
        iteration: int,
        next_open: datetime,
        sleep_seconds: int,
    ) -> None:
        """
        Records a normal idle heartbeat.

        An idle market state is not an error and must not increase
        the failed-iteration counter.
        """

        self.health.status = "IDLE"
        self.health.current_iteration = iteration
        self.health.last_heartbeat_at = self.clock()
        self.health.last_error = None

        self._record(
            "MARKETS_IDLE",
            (
                "All configured markets are closed. "
                f"Next market open: {next_open.isoformat()}. "
                f"Next check in {sleep_seconds} seconds."
            ),
            iteration=iteration,
        )

    def runtime_stopped(
        self,
        reason: str,
    ) -> None:
        now = self.clock()

        self.health.status = "STOPPED"
        self.health.stopped_at = now
        self.health.last_heartbeat_at = now

        self._record(
            "RUNTIME_STOPPED",
            reason,
        )

    def _update_session_counts(
        self,
        result: AutonomousPaperTradingResult,
    ) -> None:
        session = result.session

        self.health.open_positions = len(
            session.portfolio.positions
        )
        self.health.position_states = len(
            session.position_states
        )
        self.health.risk_plans = len(
            session.risk_plans
        )
        self.health.risk_evaluations = (
            result.risk_evaluations
        )
        self.health.risk_rejections = (
            result.risk_rejections
        )

    def _record(
        self,
        event_type: str,
        message: str,
        iteration: int | None = None,
        duration_seconds: float | None = None,
        error: str | None = None,
    ) -> None:
        if self.event_repository is None:
            return

        self.event_repository.append(
            RuntimeEvent(
                timestamp=self.clock(),
                event_type=event_type,
                status=self.health.status,
                iteration=(
                    self.health.current_iteration
                    if iteration is None
                    else iteration
                ),
                message=message,
                duration_seconds=duration_seconds,
                open_positions=self.health.open_positions,
                position_states=self.health.position_states,
                risk_plans=self.health.risk_plans,
                risk_evaluations=(
                    self.health.risk_evaluations
                ),
                risk_rejections=(
                    self.health.risk_rejections
                ),
                error=error,
            )
        )
