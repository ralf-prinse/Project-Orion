from core.container import ApplicationContainer, ServiceRegistry
from core.orchestration import ScanOrchestrator


class FakePipeline:
    def run(self, symbols):
        return object()


def test_application_container_registers_core_scan_services():
    container = ApplicationContainer()

    registered_names = container.registry.registered_names()

    assert ApplicationContainer.SCAN_PIPELINE in registered_names
    assert ApplicationContainer.SCAN_ORCHESTRATOR in registered_names


def test_application_container_resolves_scan_orchestrator_as_singleton():
    registry = ServiceRegistry()
    registry.register_singleton(
        ApplicationContainer.SCAN_PIPELINE,
        FakePipeline,
    )
    container = ApplicationContainer(registry=registry)

    first = container.scan_orchestrator()
    second = container.scan_orchestrator()

    assert isinstance(first, ScanOrchestrator)
    assert first is second


def test_application_container_injects_scan_pipeline_into_orchestrator():
    fake_pipeline = FakePipeline()
    registry = ServiceRegistry()
    registry.register_singleton(
        ApplicationContainer.SCAN_PIPELINE,
        lambda: fake_pipeline,
    )

    container = ApplicationContainer(registry=registry)
    orchestrator = container.scan_orchestrator()

    assert orchestrator.scan_pipeline is fake_pipeline


def test_application_container_preserves_preconfigured_orchestrator_registration():
    custom_orchestrator = object()
    registry = ServiceRegistry()
    registry.register_singleton(
        ApplicationContainer.SCAN_ORCHESTRATOR,
        lambda: custom_orchestrator,
    )

    container = ApplicationContainer(registry=registry)

    assert container.scan_orchestrator() is custom_orchestrator


def test_application_container_resolves_registered_service_by_name():
    fake_pipeline = FakePipeline()
    registry = ServiceRegistry()
    registry.register_singleton("custom", lambda: fake_pipeline)

    container = ApplicationContainer(registry=registry)

    assert container.resolve("custom") is fake_pipeline


def test_application_container_replaces_singleton_registration():
    first_pipeline = FakePipeline()
    second_pipeline = FakePipeline()
    registry = ServiceRegistry()
    registry.register_singleton(
        ApplicationContainer.SCAN_PIPELINE,
        lambda: first_pipeline,
    )
    container = ApplicationContainer(registry=registry)

    assert container.scan_pipeline() is first_pipeline

    container.replace_singleton(
        ApplicationContainer.SCAN_PIPELINE,
        lambda: second_pipeline,
    )

    assert container.scan_pipeline() is second_pipeline


def test_application_container_replaces_transient_registration():
    registry = ServiceRegistry()
    registry.register_singleton("custom", FakePipeline)
    container = ApplicationContainer(registry=registry)

    container.replace_transient("custom", FakePipeline)

    first = container.resolve("custom")
    second = container.resolve("custom")

    assert isinstance(first, FakePipeline)
    assert isinstance(second, FakePipeline)
    assert first is not second


def test_application_container_registers_event_bus():
    from core.events import EventBus

    container = ApplicationContainer()

    assert ApplicationContainer.EVENT_BUS in container.registry.registered_names()
    assert isinstance(container.event_bus(), EventBus)


def test_application_container_injects_event_bus_into_orchestrator():
    from core.events import EventBus

    event_bus = EventBus()
    registry = ServiceRegistry()
    registry.register_singleton(
        ApplicationContainer.EVENT_BUS,
        lambda: event_bus,
    )
    registry.register_singleton(
        ApplicationContainer.SCAN_PIPELINE,
        FakePipeline,
    )

    container = ApplicationContainer(registry=registry)
    orchestrator = container.scan_orchestrator()

    assert orchestrator.event_bus is event_bus
