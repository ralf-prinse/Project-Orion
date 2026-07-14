from datetime import UTC, datetime
from unittest.mock import patch

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.continuous_runner_config import (
    ContinuousRunnerConfig,
)
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)
from services.market_session_service import (
    MarketSessionService,
)
from services.runtime_supervisor import (
    RuntimeSupervisor,
)


class FailIfCalledRunner:
    def __init__(self):
        self.calls = 0

    def run(self):
        self.calls += 1

        raise AssertionError(
            "Autonomous runner must not run "
            "while all markets are closed."
        )


class EventRepository:
    def __init__(self):
        self.events = []

    def append(
        self,
        event,
    ):
        self.events.append(event)


def test_continuous_runner_idles_when_all_markets_closed():
    closed_time = datetime(
        2026,
        7,
        15,
        2,
        0,
        tzinfo=UTC,
    )

    autonomous_runner = FailIfCalledRunner()
    event_repository = EventRepository()

    supervisor = RuntimeSupervisor(
        event_repository=event_repository,
        clock=lambda: closed_time,
    )

    config = ContinuousRunnerConfig(
        autonomous_config=(
            AutonomousPaperTradingConfig(
                cycles=1,
                sleep_seconds=0,
            )
        ),
        interval_seconds=1,
        max_iterations=1,
        stop_on_exception=False,
        print_iteration_summary=False,
    )

    continuous_runner = (
        ContinuousPaperTradingRunner(
            config=config,
            runner=autonomous_runner,
            supervisor=supervisor,
            market_session_service=(
                MarketSessionService()
            ),
            clock=lambda: closed_time,
        )
    )

    with patch(
        "services.continuous_paper_trading_runner.time.sleep"
    ) as mocked_sleep:
        result = continuous_runner.run()

    assert autonomous_runner.calls == 0

    assert result.iterations_completed == 0
    assert result.failed_iterations == 0
    assert result.idle_iterations == 1
    assert result.last_result is None

    assert mocked_sleep.call_count == 0

    event_types = [
        event.event_type
        for event in event_repository.events
    ]

    assert event_types == [
        "RUNTIME_STARTED",
        "MARKETS_IDLE",
        "RUNTIME_STOPPED",
    ]

    idle_event = event_repository.events[1]

    assert idle_event.status == "IDLE"
    assert idle_event.error is None

    print("CONTINUOUS MARKET IDLE: PASS")


def run():
    test_continuous_runner_idles_when_all_markets_closed()


if __name__ == "__main__":
    run()