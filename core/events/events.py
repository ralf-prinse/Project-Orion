from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.events.event import Event


@dataclass(frozen=True)
class ScanStartedEvent(Event):
    symbols: list[str] = field(default_factory=list)

    def __init__(self, symbols: list[str]):
        object.__setattr__(self, "name", "scan.started")
        object.__setattr__(self, "payload", {"symbols": list(symbols)})
        object.__setattr__(self, "symbols", list(symbols))


@dataclass(frozen=True)
class PipelineStepStartedEvent(Event):
    step_name: str = ""
    index: int = 0
    total: int = 0

    def __init__(self, step_name: str, index: int, total: int):
        object.__setattr__(self, "name", "pipeline.step.started")
        object.__setattr__(
            self,
            "payload",
            {
                "step_name": step_name,
                "index": int(index),
                "total": int(total),
            },
        )
        object.__setattr__(self, "step_name", step_name)
        object.__setattr__(self, "index", int(index))
        object.__setattr__(self, "total", int(total))


@dataclass(frozen=True)
class PipelineStepCompletedEvent(Event):
    step_name: str = ""
    index: int = 0
    total: int = 0
    duration_seconds: float = 0.0

    def __init__(
        self,
        step_name: str,
        index: int,
        total: int,
        duration_seconds: float,
    ):
        rounded_duration = round(float(duration_seconds), 6)
        object.__setattr__(self, "name", "pipeline.step.completed")
        object.__setattr__(
            self,
            "payload",
            {
                "step_name": step_name,
                "index": int(index),
                "total": int(total),
                "duration_seconds": rounded_duration,
            },
        )
        object.__setattr__(self, "step_name", step_name)
        object.__setattr__(self, "index", int(index))
        object.__setattr__(self, "total", int(total))
        object.__setattr__(self, "duration_seconds", rounded_duration)


@dataclass(frozen=True)
class PipelineFailedEvent(Event):
    error_message: str = ""
    exception_type: str = ""

    def __init__(self, error_message: str, exception_type: str = ""):
        object.__setattr__(self, "name", "pipeline.failed")
        object.__setattr__(
            self,
            "payload",
            {
                "error_message": error_message,
                "exception_type": exception_type,
            },
        )
        object.__setattr__(self, "error_message", error_message)
        object.__setattr__(self, "exception_type", exception_type)


@dataclass(frozen=True)
class ScanCompletedEvent(Event):
    summary: Any = None
    success: bool = False

    def __init__(self, summary: Any):
        success = bool(getattr(summary, "success", False))
        object.__setattr__(self, "name", "scan.completed")
        object.__setattr__(
            self,
            "payload",
            {
                "summary": summary,
                "success": success,
            },
        )
        object.__setattr__(self, "summary", summary)
        object.__setattr__(self, "success", success)
