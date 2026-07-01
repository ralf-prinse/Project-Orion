from dataclasses import dataclass, field
from typing import Any

from core.orchestration.scan_statistics import ScanStatistics


@dataclass
class ScanSummary:
    """
    Public result returned by ScanOrchestrator.

    It provides one stable entrypoint result for GUI, CLI, future schedulers,
    API endpoints and automated workflows. Domain-specific objects are kept as
    opaque payloads so the orchestrator does not need to know their internals.
    """

    opportunities: list[Any] = field(default_factory=list)
    pipeline_status: Any | None = None
    statistics: ScanStatistics = field(default_factory=ScanStatistics)

    @property
    def success(self) -> bool:
        return self.statistics.success

    @property
    def errors(self) -> list[str]:
        return self.statistics.errors

    @property
    def messages(self) -> list[str]:
        return self.statistics.messages

    @property
    def opportunities_count(self) -> int:
        return len(self.opportunities)
