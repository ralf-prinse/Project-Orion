from pathlib import Path

from run_continuous_restart_smoke import (
    SESSION_PATH,
    build_runner,
    build_seed_session,
    validate_managed_session,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


TEST_PATH = Path("output/test_smoke_trading_session.json")


def test_seed_session_is_complete():
    session = build_seed_session()

    assert "AAPL" in session.portfolio.positions
    assert "AAPL" in session.position_states
    assert "AAPL" in session.risk_plans


def test_continuous_runner_persists_managed_lifecycle_across_restart():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()
    repository.save(build_seed_session())

    first_runner = build_runner(
        repository=repository,
        iterations=1,
        interval=1,
        price=106.0,
    )

    first_result = first_runner.run()

    assert first_result.iterations_completed == 1
    assert first_result.failed_iterations == 0

    first_persisted = repository.load()
    validate_managed_session(first_persisted)

    first_stop = first_persisted.position_states[
        "AAPL"
    ].current_stop_loss

    second_runner = build_runner(
        repository=repository,
        iterations=1,
        interval=1,
        price=106.0,
    )

    second_result = second_runner.run()

    assert second_result.iterations_completed == 1
    assert second_result.failed_iterations == 0

    second_persisted = repository.load()
    validate_managed_session(second_persisted)

    second_stop = second_persisted.position_states[
        "AAPL"
    ].current_stop_loss

    assert second_stop == first_stop

    repository.delete()


def test_smoke_path_is_isolated():
    assert str(SESSION_PATH).replace("\\\\", "/") == (
        "data/smoke_trading_session.json"
    )


def main():
    print()
    print("=========================================")
    print("CONTINUOUS RESTART SMOKE TEST")
    print("=========================================")
    print()

    test_seed_session_is_complete()
    test_continuous_runner_persists_managed_lifecycle_across_restart()
    test_smoke_path_is_isolated()

    print("CONTINUOUS RESTART SMOKE: PASS")


if __name__ == "__main__":
    main()
