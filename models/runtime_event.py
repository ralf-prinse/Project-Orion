from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RuntimeEvent:
    timestamp: datetime
    event_type: str
    status: str
    iteration: int
    message: str
    duration_seconds: float | None = None
    open_positions: int | None = None
    position_states: int | None = None
    risk_plans: int | None = None
    error: str | None = None
