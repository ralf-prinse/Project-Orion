from __future__ import annotations

from dataclasses import dataclass

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)


@dataclass(frozen=True)
class ContinuousRunnerConfig:
    """
    Configuration for the long-running paper trading runner.

    The continuous runner repeatedly executes finite autonomous
    paper-trading runs until stopped.

    It never changes trading strategy configuration automatically.
    """

    autonomous_config: AutonomousPaperTradingConfig

    interval_seconds: int = 300

    max_iterations: int | None = None

    stop_on_exception: bool = False

    print_iteration_summary: bool = True

    def __post_init__(self):
        if self.interval_seconds < 1:
            raise ValueError("interval_seconds must be at least 1.")

        if (
            self.max_iterations is not None
            and self.max_iterations < 1
        ):
            raise ValueError("max_iterations must be at least 1.")