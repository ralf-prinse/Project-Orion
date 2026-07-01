from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.events.event import Event
from core.events.events import (
    PipelineFailedEvent,
    PipelineStepCompletedEvent,
    PipelineStepStartedEvent,
    ScanCompletedEvent,
    ScanStartedEvent,
)


@dataclass(frozen=True)
class EventLogEntry:
    """
    Deterministic in-memory log entry generated from an Orion event.

    The first logging listener intentionally keeps logging in memory instead of
    writing to disk. File logging, rotation and user-facing diagnostics can be
    added later without changing the EventBus or ScanOrchestrator.
    """

    event_name: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)


class LoggingListener:
    """
    Event listener that converts core events into deterministic log entries.

    This listener is deliberately small and side-effect free. It records log
    entries in memory so tests, diagnostics and future GUI panels can inspect
    what happened during a scan without coupling directly to orchestration code.
    """

    def __init__(self) -> None:
        self._entries: list[EventLogEntry] = []

    def __call__(self, event: Event) -> None:
        self.handle(event)

    def handle(self, event: Event) -> None:
        if not isinstance(event, Event):
            raise TypeError("LoggingListener can only handle Event instances.")

        self._entries.append(
            EventLogEntry(
                event_name=event.name,
                message=self._message_for(event),
                payload=dict(event.payload),
            )
        )

    def entries(self) -> list[EventLogEntry]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()

    def _message_for(self, event: Event) -> str:
        if isinstance(event, ScanStartedEvent):
            return f"Scan started for {len(event.symbols)} symbols."

        if isinstance(event, PipelineStepStartedEvent):
            return f"Pipeline step started: {event.step_name} ({event.index}/{event.total})."

        if isinstance(event, PipelineStepCompletedEvent):
            return (
                f"Pipeline step completed: {event.step_name} "
                f"in {event.duration_seconds:.6f}s."
            )

        if isinstance(event, PipelineFailedEvent):
            return f"Pipeline failed: {event.error_message}"

        if isinstance(event, ScanCompletedEvent):
            status = "success" if event.success else "failed"
            return f"Scan completed with status: {status}."

        return f"Event received: {event.name}"


@dataclass(frozen=True)
class StepMetric:
    """Timing metric for a completed pipeline step."""

    step_name: str
    duration_seconds: float


class MetricsListener:
    """
    Event listener that tracks deterministic scan and pipeline metrics.

    Metrics are intentionally stored in memory. This keeps the first integration
    simple while preparing Orion for future GUI dashboards, diagnostics and
    persistent operational metrics.
    """

    def __init__(self) -> None:
        self.reset()

    def __call__(self, event: Event) -> None:
        self.handle(event)

    def handle(self, event: Event) -> None:
        if not isinstance(event, Event):
            raise TypeError("MetricsListener can only handle Event instances.")

        if isinstance(event, ScanStartedEvent):
            self.scans_started += 1
            self.last_scan_symbols = list(event.symbols)
            return

        if isinstance(event, PipelineStepStartedEvent):
            self.pipeline_steps_started += 1
            return

        if isinstance(event, PipelineStepCompletedEvent):
            self.pipeline_steps_completed += 1
            self.step_metrics.append(
                StepMetric(
                    step_name=event.step_name,
                    duration_seconds=event.duration_seconds,
                )
            )
            return

        if isinstance(event, PipelineFailedEvent):
            self.failures += 1
            self.last_error_message = event.error_message
            return

        if isinstance(event, ScanCompletedEvent):
            self.scans_completed += 1
            self.last_scan_success = event.success
            return

    def reset(self) -> None:
        self.scans_started = 0
        self.scans_completed = 0
        self.pipeline_steps_started = 0
        self.pipeline_steps_completed = 0
        self.failures = 0
        self.last_scan_success: bool | None = None
        self.last_scan_symbols: list[str] = []
        self.last_error_message: str | None = None
        self.step_metrics: list[StepMetric] = []

    @property
    def total_step_seconds(self) -> float:
        return round(sum(metric.duration_seconds for metric in self.step_metrics), 6)

    def snapshot(self) -> dict[str, Any]:
        return {
            "scans_started": self.scans_started,
            "scans_completed": self.scans_completed,
            "pipeline_steps_started": self.pipeline_steps_started,
            "pipeline_steps_completed": self.pipeline_steps_completed,
            "failures": self.failures,
            "last_scan_success": self.last_scan_success,
            "last_scan_symbols": list(self.last_scan_symbols),
            "last_error_message": self.last_error_message,
            "total_step_seconds": self.total_step_seconds,
            "step_metrics": [
                {
                    "step_name": metric.step_name,
                    "duration_seconds": metric.duration_seconds,
                }
                for metric in self.step_metrics
            ],
        }
