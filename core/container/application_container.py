from __future__ import annotations

from typing import Any

from core.container.service_registry import ServiceRegistry


class ApplicationContainer:
    """
    Composition root for Project Orion.

    The container is the only infrastructure component responsible for building
    application-level services. It starts deliberately small: Sprint 10.12.1
    centralises construction of the scan pipeline and scan orchestrator without
    forcing a risky project-wide refactor.
    """

    SCAN_PIPELINE = "scan_pipeline"
    SCAN_ORCHESTRATOR = "scan_orchestrator"

    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry()
        self._register_defaults()

    def scan_pipeline(self) -> Any:
        return self.registry.resolve(self.SCAN_PIPELINE)

    def scan_orchestrator(self) -> Any:
        return self.registry.resolve(self.SCAN_ORCHESTRATOR)

    def _register_defaults(self) -> None:
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

    def _create_scan_pipeline(self) -> Any:
        # Lazy import keeps importing core.container safe in environments where
        # optional provider/UI dependencies are unavailable.
        from services.scanner.scan_pipeline import ScanPipeline

        return ScanPipeline()

    def _create_scan_orchestrator(self) -> Any:
        from core.orchestration.scan_orchestrator import ScanOrchestrator

        return ScanOrchestrator(scan_pipeline=self.scan_pipeline())
