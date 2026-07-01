from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass
class ScanStepResult:
    """
    Result returned by one orchestration step.

    The orchestrator treats the payload as opaque data. Domain services remain
    responsible for producing their own models, while the orchestration layer
    only coordinates execution, timing, progress and summary metadata.
    """

    payload: Any = None
    opportunities: list[Any] = field(default_factory=list)
    pipeline_status: Any | None = None
    symbols_processed: int | None = None
    symbols_failed: int | None = None
    opportunities_count: int | None = None
    messages: list[str] = field(default_factory=list)


@runtime_checkable
class ScanStep(Protocol):
    """
    Protocol for deterministic scan orchestration steps.

    A scan step may wrap a full service, an engine or an existing pipeline. It
    must not contain domain logic itself. Its responsibility is limited to
    adapting an existing component to the orchestration contract.
    """

    name: str

    def run(self, payload: Any) -> ScanStepResult:
        """Run the step and return a structured orchestration result."""
