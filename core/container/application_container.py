from __future__ import annotations

from collections.abc import Callable
from typing import Any

from core.container.service_registry import ServiceRegistry


class ApplicationContainer:
    """
    Composition root for Project Orion.

    The container is the only infrastructure component responsible for building
    application-level services. It remains deliberately explicit: services are
    registered by name with factories, and callers resolve only the services
    that are part of the supported application composition.
    """

    EVENT_BUS = "event_bus"
    SCAN_PIPELINE = "scan_pipeline"
    SCAN_ORCHESTRATOR = "scan_orchestrator"

    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry()
        self._register_defaults()

    def event_bus(self) -> Any:
        return self.resolve(self.EVENT_BUS)

    def scan_pipeline(self) -> Any:
        return self.resolve(self.SCAN_PIPELINE)

    def scan_orchestrator(self) -> Any:
        return self.resolve(self.SCAN_ORCHESTRATOR)

    def resolve(self, name: str) -> Any:
        """Resolve a registered application service by name."""

        return self.registry.resolve(name)

    def replace_singleton(self, name: str, factory: Callable[[], Any]) -> None:
        """
        Replace a singleton registration.

        This is intentionally exposed for tests and future provider swaps. It
        keeps replacement logic inside the composition root instead of requiring
        callers to manipulate registry internals directly.
        """

        self.registry.replace_singleton(name, factory)

    def replace_transient(self, name: str, factory: Callable[[], Any]) -> None:
        """Replace a transient registration through the composition root."""

        self.registry.replace_transient(name, factory)

    def _register_defaults(self) -> None:
        if not self.registry.is_registered(self.EVENT_BUS):
            self.registry.register_singleton(
                self.EVENT_BUS,
                self._create_event_bus,
            )

        if not self.registry.is_registered(self.SCAN_PIPELINE):
            self.registry.register_singleton(
                self.SCAN_PIPELINE,
                self._create_scan_pipeline,
            )

        if not self.registry.is_registered(self.SCAN_ORCHESTRATOR):
            self.registry.register_singleton(
                self.SCAN_ORCHESTRATOR,
                self._create_scan_orchestrator,
            )

    def _create_event_bus(self) -> Any:
        from core.events import EventBus

        return EventBus()

    def _create_scan_pipeline(self) -> Any:
        # Lazy import keeps importing core.container safe in environments where
        # optional provider/UI dependencies are unavailable.
        from services.scanner.scan_pipeline import ScanPipeline

        return ScanPipeline()

    def _create_scan_orchestrator(self) -> Any:
        from core.orchestration.scan_orchestrator import ScanOrchestrator

        return ScanOrchestrator(
            scan_pipeline=self.scan_pipeline(),
            event_bus=self.event_bus(),
        )
