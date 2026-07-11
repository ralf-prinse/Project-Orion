from argparse import Namespace

from run_continuous_paper_trading import (
    build_runner,
    resolve_settings,
)


def test_bounded_test_defaults():
    settings = resolve_settings(
        Namespace(
            test=True,
            iterations=None,
            interval=None,
            max_symbols=None,
            initial_cash=500.0,
        )
    )

    assert settings.test_mode is True
    assert settings.max_iterations == 3
    assert settings.interval_seconds == 10
    assert settings.max_symbols == 5
    assert settings.initial_cash == 500.0


def test_explicit_test_overrides():
    settings = resolve_settings(
        Namespace(
            test=True,
            iterations=2,
            interval=1,
            max_symbols=3,
            initial_cash=750.0,
        )
    )

    assert settings.max_iterations == 2
    assert settings.interval_seconds == 1
    assert settings.max_symbols == 3
    assert settings.initial_cash == 750.0


def test_continuous_defaults():
    settings = resolve_settings(
        Namespace(
            test=False,
            iterations=None,
            interval=None,
            max_symbols=None,
            initial_cash=500.0,
        )
    )

    assert settings.test_mode is False
    assert settings.max_iterations is None
    assert settings.interval_seconds == 300
    assert settings.max_symbols == 25


def test_runner_uses_complete_session_persistence():
    settings = resolve_settings(
        Namespace(
            test=True,
            iterations=1,
            interval=1,
            max_symbols=1,
            initial_cash=500.0,
        )
    )

    runner = build_runner(settings)
    autonomous_runner = runner.runner

    assert autonomous_runner.trading_session_repository is not None
    assert (
        str(autonomous_runner.trading_session_repository.path)
        == "data\\trading_session.json"
        or str(autonomous_runner.trading_session_repository.path)
        == "data/trading_session.json"
    )

    assert autonomous_runner.portfolio_repository is not None
    assert autonomous_runner.trade_journal_repository is not None

    assert runner.config.max_iterations == 1
    assert runner.config.interval_seconds == 1
    assert (
        runner.config.autonomous_config.live_config.max_symbols
        == 1
    )


def main():
    print()
    print("=========================================")
    print("CONTINUOUS RUNNER ENTRYPOINT TEST")
    print("=========================================")
    print()

    test_bounded_test_defaults()
    test_explicit_test_overrides()
    test_continuous_defaults()
    test_runner_uses_complete_session_persistence()

    print("CONTINUOUS RUNNER ENTRYPOINT: PASS")


if __name__ == "__main__":
    main()
