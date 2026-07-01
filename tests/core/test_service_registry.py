import pytest

from core.container import ServiceRegistry


class ExampleService:
    pass


def test_service_registry_resolves_singleton_once():
    registry = ServiceRegistry()
    registry.register_singleton("example", ExampleService)

    first = registry.resolve("example")
    second = registry.resolve("example")

    assert first is second


def test_service_registry_resolves_transient_each_time():
    registry = ServiceRegistry()
    registry.register_transient("example", ExampleService)

    first = registry.resolve("example")
    second = registry.resolve("example")

    assert first is not second


def test_service_registry_reports_registered_names_deterministically():
    registry = ServiceRegistry()
    registry.register_singleton("scan_orchestrator", ExampleService)
    registry.register_singleton("analysis_engine", ExampleService)

    assert registry.registered_names() == ["analysis_engine", "scan_orchestrator"]


def test_service_registry_rejects_empty_service_name():
    registry = ServiceRegistry()

    with pytest.raises(ValueError, match="Service name cannot be empty"):
        registry.register_singleton(" ", ExampleService)


def test_service_registry_rejects_non_callable_factory():
    registry = ServiceRegistry()

    with pytest.raises(TypeError, match="Service factory must be callable"):
        registry.register_singleton("example", object())


def test_service_registry_raises_clear_error_for_missing_service():
    registry = ServiceRegistry()

    with pytest.raises(KeyError, match="Service is not registered: missing"):
        registry.resolve("missing")
