from __future__ import annotations

import time
from dataclasses import dataclass

from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)


@dataclass(frozen=True)
class ContinuousPaperTradingRunResult:
    """
    Result of one continuous runner session.

    This result describes the runner session itself, not a trading
    strategy result.
    """

    iterations_completed: int
    failed_iterations: int
    last_result: AutonomousPaperTradingResult | None


class ContinuousPaperTradingRunner:
    """
    Long-running paper trading runner.

    Responsibilities:
    - repeatedly run AutonomousPaperTradingRunner
    - classify autonomous results as successful or failed iterations
    - continue from repository-backed state after recoverable failures
    - wait between iterations
    - stop cleanly on KeyboardInterrupt
    - optionally stop on failures

    Does NOT:
    - generate trading decisions
    - allocate capital directly
    - execute trades directly
    - modify strategy configuration
    """

    def __init__(
        self,
        config: ContinuousRunnerConfig,
        runner: AutonomousPaperTradingRunner | None = None,
    ):
        self.config = config
        self.runner = runner or AutonomousPaperTradingRunner(
            config=config.autonomous_config,
        )

    def run(self) -> ContinuousPaperTradingRunResult:
        iterations_completed = 0
        failed_iterations = 0
        last_result: AutonomousPaperTradingResult | None = None

        iteration = 0

        while self._should_continue(iteration):
            should_stop = False

            try:
                print("\n>>> Starting autonomous runner...")
                print(f">>> Iteration: {iteration + 1}")

                current_result = self.runner.run()
                last_result = current_result

                if current_result.failed_cycles > 0:
                    failed_iterations += 1

                    print(
                        ">>> Autonomous runner finished with "
                        f"{current_result.failed_cycles} failed cycle(s)."
                    )

                    if self.config.print_iteration_summary:
                        self._print_iteration_summary(
                            iteration=iteration + 1,
                            result=current_result,
                            iteration_status="FAILED",
                        )

                    should_stop = self.config.stop_on_exception
                else:
                    iterations_completed += 1

                    print(">>> Autonomous runner finished.")

                    if self.config.print_iteration_summary:
                        self._print_iteration_summary(
                            iteration=iteration + 1,
                            result=current_result,
                            iteration_status="COMPLETED",
                        )

            except KeyboardInterrupt:
                print("\n>>> KeyboardInterrupt received.")
                break

            except Exception as exc:
                failed_iterations += 1

                print("\n>>> Autonomous runner raised exception:")
                print(repr(exc))

                should_stop = self.config.stop_on_exception

            iteration += 1

            if should_stop:
                break

            if self._should_continue(iteration):
                print(
                    f">>> Sleeping for "
                    f"{self.config.interval_seconds} seconds..."
                )
                time.sleep(self.config.interval_seconds)

        return ContinuousPaperTradingRunResult(
            iterations_completed=iterations_completed,
            failed_iterations=failed_iterations,
            last_result=last_result,
        )

    def _should_continue(
        self,
        iteration: int,
    ) -> bool:
        if self.config.max_iterations is None:
            return True

        return iteration < self.config.max_iterations

    def _print_iteration_summary(
        self,
        iteration: int,
        result: AutonomousPaperTradingResult,
        iteration_status: str,
    ) -> None:
        print(
            f"Continuous iteration {iteration}: "
            f"status={iteration_status}, "
            f"completed_cycles={result.completed_cycles}, "
            f"failed_cycles={result.failed_cycles}, "
            f"cash=€{result.final_cash:.2f}, "
            f"equity=€{result.final_equity:.2f}, "
            f"open_positions={len(result.session.portfolio.positions)}"
        )
