import pytest

from core.events import (
    Event,
    EventBus,
    EventRegistry,
    PipelineFailedEvent,
    PipelineStepCompletedEvent,
    PipelineStepStartedEvent,
    ScanCompletedEvent,
    ScanStartedEvent,
)
from core.orchestration import ScanSummary


def test_event_bus_publishes_events_to_subscribers_in_order():
    bus = EventBus()
    received = []

    bus.subscribe(ScanStartedEvent, received.append)

    event = ScanStartedEvent(symbols=["AAPL", "MSFT"])
    bus.publish(event)

    assert received == [event]
    assert bus.published_events() == [event]


def test_event_bus_only_delivers_matching_event_type():
    bus = EventBus()
    received = []

    bus.subscribe(ScanCompletedEvent, received.append)
    bus.publish(ScanStartedEvent(symbols=["AAPL"]))

    assert received == []


def test_event_bus_supports_unsubscribe():
    bus = EventBus()
    received = []

    bus.subscribe(ScanStartedEvent, received.append)
    bus.unsubscribe(ScanStartedEvent, received.append)
    bus.publish(ScanStartedEvent(symbols=["AAPL"]))

    assert received == []


def test_event_bus_rejects_non_event_publications():
    bus = EventBus()

    with pytest.raises(TypeError, match="Event"):
        bus.publish(object())


def test_event_registry_ignores_duplicate_handler_subscription():
    registry = EventRegistry()
    received = []

    registry.subscribe(ScanStartedEvent, received.append)
    registry.subscribe(ScanStartedEvent, received.append)

    assert registry.handler_count(ScanStartedEvent) == 1


def test_event_models_expose_deterministic_payloads():
    started = ScanStartedEvent(symbols=["aapl"])
    step_started = PipelineStepStartedEvent(
        step_name="analysis",
        index=1,
        total=3,
    )
    step_completed = PipelineStepCompletedEvent(
        step_name="analysis",
        index=1,
        total=3,
        duration_seconds=1.23456789,
    )
    failed = PipelineFailedEvent(
        error_message="Scan failed",
        exception_type="RuntimeError",
    )
    completed = ScanCompletedEvent(summary=ScanSummary())

    assert started.name == "scan.started"
    assert started.payload["symbols"] == ["aapl"]
    assert step_started.payload["step_name"] == "analysis"
    assert step_completed.duration_seconds == 1.234568
    assert failed.payload["exception_type"] == "RuntimeError"
    assert completed.name == "scan.completed"
    assert completed.success is True


def test_event_registry_rejects_invalid_event_types_and_handlers():
    registry = EventRegistry()

    with pytest.raises(TypeError, match="Event subclass"):
        registry.subscribe(object, lambda event: None)

    with pytest.raises(TypeError, match="callable"):
        registry.subscribe(Event, object())
