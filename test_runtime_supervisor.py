from datetime import datetime, timedelta

from models.autonomous_paper_trading_result import AutonomousPaperTradingResult
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.runtime_supervisor import RuntimeSupervisor


class InMemoryRuntimeEventRepository:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)


class Clock:
    def __init__(self):
        self.current = datetime(2026, 7, 11, 12, 0, 0)

    def __call__(self):
        value = self.current
        self.current += timedelta(seconds=1)
        return value


def build_result(failed_cycles=0):
    session = TradingSession(
        name="Runtime Supervisor Test",
        portfolio=PaperPortfolio(cash=500.0),
    )
    return AutonomousPaperTradingResult(
        session=session,
        cycle_results=[],
        completed_cycles=0 if failed_cycles else 1,
        failed_cycles=failed_cycles,
        initial_cash=500.0,
        final_cash=500.0,
        final_equity=500.0,
    )


def test_supervisor_records_successful_runtime():
    repository = InMemoryRuntimeEventRepository()
    supervisor = RuntimeSupervisor(
        event_repository=repository,
        clock=Clock(),
    )

    supervisor.runtime_started()
    supervisor.iteration_started(1)
    supervisor.iteration_completed(1, build_result(), 0.25)
    supervisor.runtime_stopped("Completed.")

    health = supervisor.health
    assert health.status == "STOPPED"
    assert health.iterations_completed == 1
    assert health.failed_iterations == 0
    assert health.current_iteration == 1
    assert health.last_iteration_duration_seconds == 0.25
    assert [event.event_type for event in repository.events] == [
        "RUNTIME_STARTED",
        "ITERATION_STARTED",
        "ITERATION_COMPLETED",
        "RUNTIME_STOPPED",
    ]


def test_supervisor_records_exception_failure():
    repository = InMemoryRuntimeEventRepository()
    supervisor = RuntimeSupervisor(
        event_repository=repository,
        clock=Clock(),
    )

    supervisor.runtime_started()
    supervisor.iteration_started(1)
    error = RuntimeError("boom")
    supervisor.iteration_failed(1, 0.5, error=error)

    assert supervisor.health.failed_iterations == 1
    assert supervisor.health.last_error == "RuntimeError('boom')"
    assert repository.events[-1].event_type == "ITERATION_FAILED"
    assert repository.events[-1].error == "RuntimeError('boom')"


def main():
    test_supervisor_records_successful_runtime()
    test_supervisor_records_exception_failure()
    print("RUNTIME SUPERVISOR: PASS")


if __name__ == "__main__":
    main()
