from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScanStageTiming:
    """
    Timing measurement for one orchestration stage.
    """

    stage: str
    duration_seconds: float


@dataclass
class ScanStatistics:
    """
    Runtime statistics for one complete Orion scan.

    This model is intentionally generic. It can represent the current scanner
    pipeline and can later be extended by the decision, planner, paper trading,
    backtesting or GUI integration layers without changing the public
    ScanOrchestrator API.
    """

    symbols_requested: int = 0
    symbols_processed: int = 0
    symbols_failed: int = 0
    opportunities_count: int = 0
    total_seconds: float = 0.0

    timings: list[ScanStageTiming] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def add_timing(self, stage: str, duration_seconds: float) -> None:
        self.timings.append(
            ScanStageTiming(
                stage=stage,
                duration_seconds=round(float(duration_seconds), 6),
            )
        )

    def add_message(self, message: str) -> None:
        if message:
            self.messages.append(message)

    def add_error(self, error: str) -> None:
        if error:
            self.errors.append(error)

    @property
    def success(self) -> bool:
        return not self.errors
