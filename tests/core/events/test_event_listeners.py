import pytest

from core.events import (
    LoggingListener,
    MetricsListener,
    PipelineFailedEvent,
    PipelineStepCompletedEvent,
    PipelineStepStartedEvent,
    ScanCompletedEvent,
    ScanStartedEvent,
)
from core.orchestration import ScanSummary


def test_logging_listener_records_deterministic_log_entries():
    listener = LoggingListener()

    listener.handle(ScanStartedEvent(symbols=["AAPL", "MSFT"]))
    listener.handle(
        PipelineStepCompletedEvent(
            step_name="analysis",
            index=1,
            total=2,
            duration_seconds=1.23456789,
        )
    )
    listener.handle(ScanCompletedEvent(summary=ScanSummary()))

    entries = listener.entries()

    assert [entry.event_name for entry in entries] == [
        "scan.started",
        "pipeline.step.completed",
        "scan.completed",
    ]
    assert entries[0].message == "Scan started for 2 symbols."
    assert entries[1].message == "Pipeline step completed: analysis in 1.234568s."
    assert entries[2].message == "Scan completed with status: success."


def test_logging_listener_rejects_non_events():
    listener = LoggingListener()

    with pytest.raises(TypeError, match="Event"):
        listener.handle(object())


def test_metrics_listener_tracks_scan_lifecycle():
    listener = MetricsListener()

    listener.handle(ScanStartedEvent(symbols=["AAPL"]))
    listener.handle(PipelineStepStartedEvent(step_name="analysis", index=1, total=1))
    listener.handle(
        PipelineStepCompletedEvent(
            step_name="analysis",
            index=1,
            total=1,
            duration_seconds=0.123456789,
        )
    )
    listener.handle(ScanCompletedEvent(summary=ScanSummary()))

    snapshot = listener.snapshot()

    assert snapshot["scans_started"] == 1
    assert snapshot["scans_completed"] == 1
    assert snapshot["pipeline_steps_started"] == 1
    assert snapshot["pipeline_steps_completed"] == 1
    assert snapshot["last_scan_success"] is True
    assert snapshot["last_scan_symbols"] == ["AAPL"]
    assert snapshot["total_step_seconds"] == 0.123457
    assert snapshot["step_metrics"] == [
        {"step_name": "analysis", "duration_seconds": 0.123457}
    ]


def test_metrics_listener_tracks_failures_and_can_reset():
    listener = MetricsListener()

    listener.handle(PipelineFailedEvent(error_message="provider unavailable"))

    assert listener.failures == 1
    assert listener.last_error_message == "provider unavailable"

    listener.reset()

    assert listener.snapshot() == {
        "scans_started": 0,
        "scans_completed": 0,
        "pipeline_steps_started": 0,
        "pipeline_steps_completed": 0,
        "failures": 0,
        "last_scan_success": None,
        "last_scan_symbols": [],
        "last_error_message": None,
        "total_step_seconds": 0,
        "step_metrics": [],
    }


def test_metrics_listener_rejects_non_events():
    listener = MetricsListener()

    with pytest.raises(TypeError, match="Event"):
        listener.handle(object())
