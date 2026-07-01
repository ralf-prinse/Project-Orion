from core.container import ApplicationContainer
from core.events import LoggingListener, MetricsListener
from core.orchestration import ScanOrchestrator, ScanStepResult


class SimpleStep:
    name = "simple_step"

    def run(self, payload):
        return ScanStepResult(payload=payload, symbols_processed=len(payload))


def test_application_container_registers_default_event_listeners():
    container = ApplicationContainer()

    registered_names = container.registry.registered_names()

    assert ApplicationContainer.EVENT_LOGGING_LISTENER in registered_names
    assert ApplicationContainer.EVENT_METRICS_LISTENER in registered_names
    assert isinstance(container.event_logging_listener(), LoggingListener)
    assert isinstance(container.event_metrics_listener(), MetricsListener)


def test_application_container_wires_event_listeners_to_event_bus():
    container = ApplicationContainer()
    bus = container.event_bus()
    logging_listener = container.event_logging_listener()
    metrics_listener = container.event_metrics_listener()

    orchestrator = ScanOrchestrator(
        scan_steps=[SimpleStep()],
        clock=lambda: 1.0,
        event_bus=bus,
    )

    summary = orchestrator.run(["AAPL"])

    assert summary.success is True
    assert [entry.event_name for entry in logging_listener.entries()] == [
        "scan.started",
        "pipeline.step.started",
        "pipeline.step.completed",
        "scan.completed",
    ]
    assert metrics_listener.snapshot()["scans_started"] == 1
    assert metrics_listener.snapshot()["scans_completed"] == 1
    assert metrics_listener.snapshot()["pipeline_steps_completed"] == 1
