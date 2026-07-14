from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.continuous_runner_config import (
    ContinuousRunnerConfig,
)
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.market_session_service import (
    MarketSessionService,
)
from services.runtime_supervisor import (
    RuntimeSupervisor,
)


@dataclass(frozen=True)
class ContinuousPaperTradingRunResult:
    iterations_completed: int
    failed_iterations: int
    last_result: AutonomousPaperTradingResult | None
    idle_iterations: int = 0


class ContinuousPaperTradingRunner:
    """
    Repeatedly executes the finite autonomous paper-trading runner.

    When a MarketSessionService is supplied and every configured
    market is closed, the runtime enters a normal IDLE state.

    During IDLE:

    - no scanner is executed;
    - no positions are revalued;
    - no BUY or SELL is executed;
    - no failed iteration is registered;
    - TradingSession remains unchanged;
    - the runtime periodically checks for the next market opening.
    """

    MAXIMUM_IDLE_POLL_SECONDS = 900

    def __init__(
        self,
        config: ContinuousRunnerConfig,
        runner: AutonomousPaperTradingRunner | None = None,
        supervisor: RuntimeSupervisor | None = None,
        market_session_service: MarketSessionService | None = None,
        clock: Callable[[], datetime] | None = None,
    ):
        self.config = config

        self.runner = (
            runner
            or AutonomousPaperTradingRunner(
                config=config.autonomous_config,
            )
        )

        self.supervisor = supervisor

        self.market_session_service = (
            market_session_service
        )

        self.clock = (
            clock
            or (
                lambda: datetime.now(UTC)
            )
        )

    def run(
        self,
    ) -> ContinuousPaperTradingRunResult:
        iterations_completed = 0
        failed_iterations = 0
        idle_iterations = 0

        last_result: (
            AutonomousPaperTradingResult
            | None
        ) = None

        iteration = 0
        stop_reason = (
            "Continuous runtime completed."
        )

        if self.supervisor is not None:
            self.supervisor.runtime_started()

        while self._should_continue(iteration):
            iteration_number = iteration + 1
            now = self._as_utc(self.clock())

            if self._all_markets_closed(now):
                idle_iterations += 1

                next_open = (
                    self.market_session_service
                    .next_market_open(now=now)
                )

                sleep_seconds = (
                    self._resolve_idle_sleep_seconds(
                        now=now,
                    )
                )

                print()
                print(
                    ">>> MARKET IDLE "
                    f"{now.isoformat(timespec='seconds')}"
                )
                print(
                    ">>> All configured markets "
                    "are closed."
                )
                print(
                    ">>> Next market open: "
                    f"{next_open.isoformat()}"
                )
                print(
                    ">>> Next market check in "
                    f"{sleep_seconds} seconds."
                )

                if self.supervisor is not None:
                    self.supervisor.market_idle(
                        iteration=iteration_number,
                        next_open=next_open,
                        sleep_seconds=sleep_seconds,
                    )

                iteration += 1

                if self._should_continue(iteration):
                    if not self._sleep(
                        sleep_seconds
                    ):
                        stop_reason = (
                            "KeyboardInterrupt received "
                            "during market idle."
                        )
                        break

                continue

            should_stop = False
            iteration_started_at = now
            started_perf = time.perf_counter()

            try:
                if self.supervisor is not None:
                    self.supervisor.iteration_started(
                        iteration_number
                    )

                print()
                print(
                    ">>> HEARTBEAT START "
                    f"{iteration_started_at.isoformat(timespec='seconds')}"
                )
                print(
                    ">>> Starting autonomous runner..."
                )
                print(
                    f">>> Iteration: {iteration_number}"
                )

                current_result = self.runner.run()
                last_result = current_result

                duration_seconds = (
                    time.perf_counter()
                    - started_perf
                )

                if current_result.failed_cycles > 0:
                    failed_iterations += 1

                    print(
                        ">>> Autonomous runner "
                        "finished with "
                        f"{current_result.failed_cycles} "
                        "failed cycle(s)."
                    )

                    if (
                        self.config
                        .print_iteration_summary
                    ):
                        self._print_iteration_summary(
                            iteration=(
                                iteration_number
                            ),
                            result=current_result,
                            iteration_status="FAILED",
                            duration_seconds=(
                                duration_seconds
                            ),
                        )

                    if self.supervisor is not None:
                        self.supervisor.iteration_failed(
                            iteration=(
                                iteration_number
                            ),
                            duration_seconds=(
                                duration_seconds
                            ),
                            result=current_result,
                        )

                    should_stop = (
                        self.config
                        .stop_on_exception
                    )

                else:
                    iterations_completed += 1

                    if self.supervisor is not None:
                        self.supervisor.iteration_completed(
                            iteration=(
                                iteration_number
                            ),
                            result=current_result,
                            duration_seconds=(
                                duration_seconds
                            ),
                        )

                    print(
                        ">>> Autonomous runner "
                        "finished."
                    )

                    if (
                        self.config
                        .print_iteration_summary
                    ):
                        self._print_iteration_summary(
                            iteration=(
                                iteration_number
                            ),
                            result=current_result,
                            iteration_status=(
                                "COMPLETED"
                            ),
                            duration_seconds=(
                                duration_seconds
                            ),
                        )

                print(
                    ">>> HEARTBEAT END "
                    f"{self.clock().isoformat(timespec='seconds')}"
                )

            except KeyboardInterrupt:
                print()
                print(
                    ">>> KeyboardInterrupt received "
                    "during iteration."
                )
                print(
                    ">>> Continuous runner "
                    "stopping cleanly."
                )

                stop_reason = (
                    "KeyboardInterrupt received "
                    "during iteration."
                )

                break

            except Exception as exc:
                failed_iterations += 1

                duration_seconds = (
                    time.perf_counter()
                    - started_perf
                )

                print()
                print(
                    ">>> Autonomous runner "
                    "raised exception:"
                )
                print(repr(exc))
                print(
                    ">>> Failed iteration duration: "
                    f"{duration_seconds:.3f} seconds"
                )

                if self.supervisor is not None:
                    self.supervisor.iteration_failed(
                        iteration=(
                            iteration_number
                        ),
                        duration_seconds=(
                            duration_seconds
                        ),
                        error=exc,
                    )

                should_stop = (
                    self.config.stop_on_exception
                )

            iteration += 1

            if should_stop:
                stop_reason = (
                    "Runtime stopped after "
                    "a failed iteration."
                )
                break

            if self._should_continue(iteration):
                if not (
                    self._sleep_until_next_iteration()
                ):
                    stop_reason = (
                        "KeyboardInterrupt received "
                        "during sleep."
                    )
                    break

        if self.supervisor is not None:
            self.supervisor.runtime_stopped(
                stop_reason
            )

        return ContinuousPaperTradingRunResult(
            iterations_completed=(
                iterations_completed
            ),
            failed_iterations=failed_iterations,
            last_result=last_result,
            idle_iterations=idle_iterations,
        )

    def _all_markets_closed(
        self,
        now: datetime,
    ) -> bool:
        if self.market_session_service is None:
            return False

        return not (
            self.market_session_service
            .any_market_open(now=now)
        )

    def _resolve_idle_sleep_seconds(
        self,
        now: datetime,
    ) -> int:
        if self.market_session_service is None:
            return self.config.interval_seconds

        seconds_until_open = (
            self.market_session_service
            .seconds_until_next_market_open(
                now=now
            )
        )

        return max(
            1,
            min(
                seconds_until_open,
                self.MAXIMUM_IDLE_POLL_SECONDS,
            ),
        )

    def _should_continue(
        self,
        iteration: int,
    ) -> bool:
        if self.config.max_iterations is None:
            return True

        return (
            iteration
            < self.config.max_iterations
        )

    def _sleep_until_next_iteration(
        self,
    ) -> bool:
        print(
            ">>> Sleeping for "
            f"{self.config.interval_seconds} "
            "seconds..."
        )

        return self._sleep(
            self.config.interval_seconds
        )

    def _sleep(
        self,
        seconds: int,
    ) -> bool:
        try:
            time.sleep(seconds)

        except KeyboardInterrupt:
            print()
            print(
                ">>> KeyboardInterrupt received "
                "during sleep."
            )
            print(
                ">>> Continuous runner "
                "stopping cleanly."
            )

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
            f"completed_cycles="
            f"{result.completed_cycles}, "
            f"failed_cycles="
            f"{result.failed_cycles}, "
            f"cash=€{result.final_cash:.2f}, "
            f"equity=€{result.final_equity:.2f}, "
            f"open_positions="
            f"{len(result.session.portfolio.positions)}, "
            f"position_states="
            f"{len(result.session.position_states)}, "
            f"risk_plans="
            f"{len(result.session.risk_plans)}"
        )

    def _as_utc(
        self,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            return value.replace(
                tzinfo=UTC
            )

        return value.astimezone(UTC)