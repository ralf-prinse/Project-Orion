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


class DummyAutonomousRunner:
    def __init__(self):
        self.calls = 0

    def run(self):
        self.calls += 1

        session = TradingSession(
            name="Dummy",
            portfolio=PaperPortfolio(
                cash=100.0,
            ),
        )

        return AutonomousPaperTradingResult(
            session=session,
            cycle_results=[],
            completed_cycles=1,
            failed_cycles=0,
            initial_cash=100.0,
            final_cash=100.0,
            final_equity=100.0,
        )


def test_continuous_runner_respects_max_iterations():
    runner = DummyAutonomousRunner()

    result = ContinuousPaperTradingRunner(
        config=ContinuousRunnerConfig(
            autonomous_config=AutonomousPaperTradingConfig(
                cycles=1,
                sleep_seconds=0,
            ),
            interval_seconds=1,
            max_iterations=3,
            print_iteration_summary=False,
        ),
        runner=runner,
    ).run()

    assert runner.calls == 3
    assert result.iterations_completed == 3
    assert result.failed_iterations == 0
    assert result.last_result is not None


def test_continuous_runner_handles_failures():
    class FailingRunner:
        def run(self):
            raise RuntimeError("Boom")

    result = ContinuousPaperTradingRunner(
        config=ContinuousRunnerConfig(
            autonomous_config=AutonomousPaperTradingConfig(
                cycles=1,
                sleep_seconds=0,
            ),
            interval_seconds=1,
            max_iterations=2,
            stop_on_exception=False,
            print_iteration_summary=False,
        ),
        runner=FailingRunner(),
    ).run()

    assert result.iterations_completed == 0
    assert result.failed_iterations == 2
    assert result.last_result is None