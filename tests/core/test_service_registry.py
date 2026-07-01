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


def test_service_registry_replace_singleton_discards_cached_instance():
    registry = ServiceRegistry()
    registry.register_singleton("example", ExampleService)

    original = registry.resolve("example")

    class ReplacementService:
        pass

    registry.replace_singleton("example", ReplacementService)

    replacement = registry.resolve("example")

    assert isinstance(replacement, ReplacementService)
    assert replacement is not original


def test_service_registry_replace_transient_changes_lifetime():
    registry = ServiceRegistry()
    registry.register_singleton("example", ExampleService)

    first = registry.resolve("example")

    class ReplacementService:
        pass

    registry.replace_transient("example", ReplacementService)

    second = registry.resolve("example")
    third = registry.resolve("example")

    assert first is not second
    assert second is not third
    assert isinstance(second, ReplacementService)
    assert isinstance(third, ReplacementService)


def test_service_registry_replace_requires_existing_registration():
    registry = ServiceRegistry()

    with pytest.raises(KeyError, match="Service is not registered: missing"):
        registry.replace_singleton("missing", ExampleService)


def test_service_registry_remove_deletes_registration_and_cached_singleton():
    registry = ServiceRegistry()
    registry.register_singleton("example", ExampleService)
    registry.resolve("example")

    registry.remove("example")

    assert not registry.is_registered("example")

    with pytest.raises(KeyError, match="Service is not registered: example"):
        registry.resolve("example")


def test_service_registry_remove_requires_existing_registration():
    registry = ServiceRegistry()

    with pytest.raises(KeyError, match="Service is not registered: missing"):
        registry.remove("missing")


def test_service_registry_clear_singletons_preserves_registrations():
    registry = ServiceRegistry()
    registry.register_singleton("example", ExampleService)

    first = registry.resolve("example")
    registry.clear_singletons()
    second = registry.resolve("example")

    assert registry.is_registered("example")
    assert first is not second
