from core.events import (
    EventBus,
    PipelineFailedEvent,
    PipelineStepCompletedEvent,
    PipelineStepStartedEvent,
    ScanCompletedEvent,
    ScanStartedEvent,
)
from core.orchestration import ScanContext, ScanOrchestrator, ScanStepResult


class FakePipeline:
    def run(self, symbols):
        return type(
            "PipelineResult",
            (),
            {
                "opportunities": ["AAPL"],
                "status": type(
                    "PipelineStatus",
                    (),
                    {
                        "technical_results_count": len(symbols),
                        "opportunities_count": 1,
                        "messages": [],
                    },
                )(),
            },
        )()


class FailingPipeline:
    def run(self, symbols):
        raise RuntimeError("provider unavailable")


class FakeClock:
    def __init__(self):
        self.value = 0.0

    def __call__(self):
        self.value += 1.0
        return self.value


class SimpleStep:
    name = "simple_step"

    def run(self, payload):
        return ScanStepResult(payload=payload, symbols_processed=len(payload))


def test_scan_orchestrator_publishes_scan_lifecycle_events():
    bus = EventBus()
    orchestrator = ScanOrchestrator(
        scan_steps=[SimpleStep()],
        clock=FakeClock(),
        event_bus=bus,
    )

    summary = orchestrator.run(["AAPL"])
    event_types = [type(event) for event in bus.published_events()]

    assert summary.success is True
    assert event_types == [
        ScanStartedEvent,
        PipelineStepStartedEvent,
        PipelineStepCompletedEvent,
        ScanCompletedEvent,
    ]
    assert bus.published_events()[0].symbols == ["AAPL"]
    assert bus.published_events()[1].step_name == "simple_step"
    assert bus.published_events()[2].duration_seconds == 1.0
    assert bus.published_events()[-1].summary is summary


def test_scan_orchestrator_publishes_failure_event_when_pipeline_fails():
    bus = EventBus()
    orchestrator = ScanOrchestrator(
        scan_pipeline=FailingPipeline(),
        clock=FakeClock(),
        event_bus=bus,
    )

    summary = orchestrator.run(ScanContext(symbols=["AAPL"], continue_on_error=True))
    event_types = [type(event) for event in bus.published_events()]

    assert summary.success is False
    assert PipelineFailedEvent in event_types
    assert event_types[-1] is ScanCompletedEvent
    failure_events = [
        event for event in bus.published_events() if isinstance(event, PipelineFailedEvent)
    ]
    assert failure_events[0].exception_type == "RuntimeError"
    assert failure_events[0].error_message == "Scan failed: provider unavailable"


def test_scan_orchestrator_can_run_without_event_bus():
    orchestrator = ScanOrchestrator(
        scan_pipeline=FakePipeline(),
        clock=FakeClock(),
    )

    summary = orchestrator.run(["AAPL"])

    assert summary.success is True
