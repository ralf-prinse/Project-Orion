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
