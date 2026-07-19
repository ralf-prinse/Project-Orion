from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RuntimeHealth:
    """Observable health state for the continuous paper-trading runtime.

    This model contains operational metadata only. It never owns trading,
    portfolio, position, risk-plan or persistence lifecycle state.
    """

    status: str = "STOPPED"
    started_at: datetime | None = None
    stopped_at: datetime | None = None
    last_heartbeat_at: datetime | None = None
    current_iteration: int = 0
    iterations_completed: int = 0
    failed_iterations: int = 0
    last_iteration_duration_seconds: float | None = None
    last_error: str | None = None
    open_positions: int = 0
    position_states: int = 0
    risk_plans: int = 0
    risk_evaluations: int = 0
    risk_rejections: int = 0

    @property
    def is_running(self) -> bool:
        return self.status == "RUNNING"
