from pathlib import Path

from run_continuous_restart_smoke import (
    build_runner,
    build_seed_session,
    validate_closed_session,
    validate_managed_position,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


TEST_PATH = Path(
    "output/test_restart_exit_recovery_session.json"
)


def test_seed_session_is_complete():
    session = build_seed_session()

    assert session.cash == 400.0
    assert session.equity == 500.0
    assert "AAPL" in session.portfolio.positions
    assert "AAPL" in session.position_states
    assert "AAPL" in session.risk_plans


def test_restart_executes_persisted_dynamic_stop_exit():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()
    repository.save(build_seed_session())

    activation_runner = build_runner(
        repository=repository,
        iterations=1,
        interval=1,
        price=106.0,
    )

    activation_result = activation_runner.run()

    assert activation_result.iterations_completed == 1
    assert activation_result.failed_iterations == 0

    managed_session = repository.load()
    validate_managed_position(managed_session)

    persisted_stop = managed_session.position_states[
        "AAPL"
    ].current_stop_loss

    assert persisted_stop == 100.7

    recovery_runner = build_runner(
        repository=repository,
        iterations=1,
        interval=1,
        price=100.4,
    )

    recovery_result = recovery_runner.run()

    assert recovery_result.iterations_completed == 1
    assert recovery_result.failed_iterations == 0

    closed_session = repository.load()
    validate_closed_session(closed_session)

    repository.delete()


def test_exit_is_based_on_persisted_managed_stop():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()
    repository.save(build_seed_session())

    activation_runner = build_runner(
        repository=repository,
        iterations=1,
        interval=1,
        price=106.0,
    )
    activation_runner.run()

    managed_session = repository.load()

    assert (
        managed_session.position_states[
            "AAPL"
        ].current_stop_loss
        == 100.7
    )

    assert (
        managed_session.risk_plans[
            "AAPL"
        ].stop_loss
        == 95.0
    )

    recovery_runner = build_runner(
        repository=repository,
        iterations=1,
        interval=1,
        price=100.4,
    )
    recovery_runner.run()

    closed_session = repository.load()

    assert "AAPL" not in closed_session.portfolio.positions
    assert closed_session.cash == 500.4

    repository.delete()


def main():
    print()
    print("=========================================")
    print("RESTART EXIT RECOVERY TEST")
    print("=========================================")
    print()

    test_seed_session_is_complete()
    test_restart_executes_persisted_dynamic_stop_exit()
    test_exit_is_based_on_persisted_managed_stop()

    print("RESTART EXIT RECOVERY: PASS")


if __name__ == "__main__":
    main()
