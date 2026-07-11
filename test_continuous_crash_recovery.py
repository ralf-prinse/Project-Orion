from pathlib import Path

from run_continuous_crash_recovery_smoke import (
    FailOnceScanner,
    build_runner,
    build_seed_session,
    validate_recovered_session,
    validate_seed_session,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)


TEST_PATH = Path(
    "output/test_crash_recovery_session.json"
)


def test_failed_cycle_does_not_replace_last_durable_session():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()
    repository.save(build_seed_session())

    scanner = FailOnceScanner()
    runner = build_runner(
        repository=repository,
        scanner=scanner,
    )

    result = runner.run()

    recovered = repository.load()

    validate_recovered_session(recovered)

    assert scanner.calls == 2
    assert result.iterations_completed == 1
    assert result.failed_iterations == 1
    assert result.last_result is not None
    assert result.last_result.failed_cycles == 0

    repository.delete()


def test_seed_is_unchanged_before_recovery_run():
    repository = JsonTradingSessionRepository(
        path=TEST_PATH,
    )

    repository.delete()
    repository.save(build_seed_session())

    loaded = repository.load()
    validate_seed_session(loaded)

    repository.delete()


def main():
    print()
    print("=========================================")
    print("CONTINUOUS CRASH RECOVERY TEST")
    print("=========================================")
    print()

    test_seed_is_unchanged_before_recovery_run()
    test_failed_cycle_does_not_replace_last_durable_session()

    print("CONTINUOUS CRASH RECOVERY: PASS")


if __name__ == "__main__":
    main()
