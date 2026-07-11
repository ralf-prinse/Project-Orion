from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime

from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)


@dataclass(frozen=True)
class ContinuousPaperTradingRunResult:
    iterations_completed: int
    failed_iterations: int
    last_result: AutonomousPaperTradingResult | None


class ContinuousPaperTradingRunner:
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
            iteration_started_at = datetime.now()
            started_perf = time.perf_counter()

            try:
                print()
                print(
                    ">>> HEARTBEAT START "
                    f"{iteration_started_at.isoformat(timespec='seconds')}"
                )
                print(">>> Starting autonomous runner...")
                print(f">>> Iteration: {iteration + 1}")

                current_result = self.runner.run()
                last_result = current_result
                duration_seconds = time.perf_counter() - started_perf

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
                            duration_seconds=duration_seconds,
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
                            duration_seconds=duration_seconds,
                        )

                print(
                    ">>> HEARTBEAT END "
                    f"{datetime.now().isoformat(timespec='seconds')}"
                )

            except KeyboardInterrupt:
                print()
                print(">>> KeyboardInterrupt received during iteration.")
                print(">>> Continuous runner stopping cleanly.")
                break

            except Exception as exc:
                failed_iterations += 1
                duration_seconds = time.perf_counter() - started_perf
                print()
                print(">>> Autonomous runner raised exception:")
                print(repr(exc))
                print(
                    ">>> Failed iteration duration: "
                    f"{duration_seconds:.3f} seconds"
                )
                should_stop = self.config.stop_on_exception

            iteration += 1

            if should_stop:
                break

            if self._should_continue(iteration):
                if not self._sleep_until_next_iteration():
                    break

        return ContinuousPaperTradingRunResult(
            iterations_completed=iterations_completed,
            failed_iterations=failed_iterations,
            last_result=last_result,
        )

    def _should_continue(self, iteration: int) -> bool:
        if self.config.max_iterations is None:
            return True
        return iteration < self.config.max_iterations

    def _sleep_until_next_iteration(self) -> bool:
        print(
            f">>> Sleeping for "
            f"{self.config.interval_seconds} seconds..."
        )
        try:
            time.sleep(self.config.interval_seconds)
        except KeyboardInterrupt:
            print()
            print(">>> KeyboardInterrupt received during sleep.")
            print(">>> Continuous runner stopping cleanly.")
            return False
        return True

    def _print_iteration_summary(
        self,
        iteration: int,
        result: AutonomousPaperTradingResult,
        iteration_status: str,
        duration_seconds: float,
    ) -> None:
        print(
            f"Continuous iteration {iteration}: "
            f"status={iteration_status}, "
            f"duration={duration_seconds:.3f}s, "
            f"completed_cycles={result.completed_cycles}, "
            f"failed_cycles={result.failed_cycles}, "
            f"cash=€{result.final_cash:.2f}, "
            f"equity=€{result.final_equity:.2f}, "
            f"open_positions={len(result.session.portfolio.positions)}, "
            f"position_states={len(result.session.position_states)}, "
            f"risk_plans={len(result.session.risk_plans)}"
        )
