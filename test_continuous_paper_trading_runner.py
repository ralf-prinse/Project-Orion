from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.autonomous_paper_trading_result import (
    AutonomousPaperTradingResult,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)


def build_result(
    completed_cycles: int = 1,
    failed_cycles: int = 0,
) -> AutonomousPaperTradingResult:
    session = TradingSession(
        name="Dummy",
        portfolio=PaperPortfolio(
            cash=100.0,
        ),
    )

    return AutonomousPaperTradingResult(
        session=session,
        cycle_results=[],
        completed_cycles=completed_cycles,
        failed_cycles=failed_cycles,
        initial_cash=100.0,
        final_cash=100.0,
        final_equity=100.0,
    )


class DummyAutonomousRunner:
    def __init__(self):
        self.calls = 0

    def run(self):
        self.calls += 1
        return build_result()


def build_config(
    max_iterations: int,
    stop_on_exception: bool = False,
) -> ContinuousRunnerConfig:
    return ContinuousRunnerConfig(
        autonomous_config=AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
        ),
        interval_seconds=1,
        max_iterations=max_iterations,
        stop_on_exception=stop_on_exception,
        print_iteration_summary=False,
    )


def test_continuous_runner_respects_max_iterations():
    runner = DummyAutonomousRunner()

    result = ContinuousPaperTradingRunner(
        config=build_config(max_iterations=3),
        runner=runner,
    ).run()

    assert runner.calls == 3
    assert result.iterations_completed == 3
    assert result.failed_iterations == 0
    assert result.last_result is not None


def test_continuous_runner_handles_raised_exceptions():
    class FailingRunner:
        def run(self):
            raise RuntimeError("Boom")

    result = ContinuousPaperTradingRunner(
        config=build_config(max_iterations=2),
        runner=FailingRunner(),
    ).run()

    assert result.iterations_completed == 0
    assert result.failed_iterations == 2
    assert result.last_result is None


def test_continuous_runner_counts_internal_cycle_failure():
    class InternallyFailingRunner:
        def __init__(self):
            self.calls = 0

        def run(self):
            self.calls += 1
            return build_result(
                completed_cycles=0,
                failed_cycles=1,
            )

    autonomous_runner = InternallyFailingRunner()

    result = ContinuousPaperTradingRunner(
        config=build_config(max_iterations=2),
        runner=autonomous_runner,
    ).run()

    assert autonomous_runner.calls == 2
    assert result.iterations_completed == 0
    assert result.failed_iterations == 2
    assert result.last_result is not None
    assert result.last_result.failed_cycles == 1


def test_continuous_runner_recovers_after_internal_failure():
    class RecoveringRunner:
        def __init__(self):
            self.calls = 0

        def run(self):
            self.calls += 1

            if self.calls == 1:
                return build_result(
                    completed_cycles=0,
                    failed_cycles=1,
                )

            return build_result(
                completed_cycles=1,
                failed_cycles=0,
            )

    autonomous_runner = RecoveringRunner()

    result = ContinuousPaperTradingRunner(
        config=build_config(max_iterations=2),
        runner=autonomous_runner,
    ).run()

    assert autonomous_runner.calls == 2
    assert result.iterations_completed == 1
    assert result.failed_iterations == 1
    assert result.last_result is not None
    assert result.last_result.completed_cycles == 1
    assert result.last_result.failed_cycles == 0


def test_continuous_runner_stops_on_internal_failure_when_configured():
    class InternallyFailingRunner:
        def __init__(self):
            self.calls = 0

        def run(self):
            self.calls += 1
            return build_result(
                completed_cycles=0,
                failed_cycles=1,
            )

    autonomous_runner = InternallyFailingRunner()

    result = ContinuousPaperTradingRunner(
        config=build_config(
            max_iterations=3,
            stop_on_exception=True,
        ),
        runner=autonomous_runner,
    ).run()

    assert autonomous_runner.calls == 1
    assert result.iterations_completed == 0
    assert result.failed_iterations == 1
    assert result.last_result is not None
