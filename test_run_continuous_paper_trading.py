from argparse import Namespace
from pathlib import Path

from run_continuous_paper_trading import (
    build_runner,
    resolve_settings,
)


def build_args(**overrides):
    values = {
        "test": False,
        "isolated": False,
        "iterations": None,
        "interval": None,
        "max_symbols": None,
        "initial_cash": 500.0,
        "stop_on_exception": False,
        "session_path": None,
        "portfolio_path": None,
        "journal_path": None,
    }
    values.update(overrides)
    return Namespace(**values)


def test_bounded_test_defaults():
    settings = resolve_settings(build_args(test=True))
    assert settings.test_mode is True
    assert settings.max_iterations == 3
    assert settings.interval_seconds == 10
    assert settings.max_symbols == 5


def test_isolated_paths():
    settings = resolve_settings(
        build_args(test=True, isolated=True)
    )
    assert settings.session_path == Path(
        "data/optimization_trading_session.json"
    )
    assert settings.portfolio_path == Path(
        "data/optimization_paper_portfolio.json"
    )
    assert settings.journal_path == Path(
        "data/optimization_trade_journal.jsonl"
    )


def test_explicit_paths_override_isolated_defaults():
    settings = resolve_settings(
        build_args(
            isolated=True,
            session_path=Path("output/custom_session.json"),
            portfolio_path=Path("output/custom_portfolio.json"),
            journal_path=Path("output/custom_journal.jsonl"),
        )
    )
    assert settings.session_path == Path("output/custom_session.json")
    assert settings.portfolio_path == Path("output/custom_portfolio.json")
    assert settings.journal_path == Path("output/custom_journal.jsonl")


def test_runner_uses_resolved_settings():
    settings = resolve_settings(
        build_args(
            test=True,
            isolated=True,
            iterations=1,
            interval=1,
            max_symbols=1,
            stop_on_exception=True,
        )
    )
    runner = build_runner(settings)
    autonomous_runner = runner.runner

    assert autonomous_runner.trading_session_repository.path == settings.session_path
    assert autonomous_runner.portfolio_repository.path == settings.portfolio_path
    assert autonomous_runner.trade_journal_repository.path == settings.journal_path
    assert runner.config.stop_on_exception is True


def main():
    print()
    print("=========================================")
    print("CONTINUOUS RUNNER ENTRYPOINT TEST")
    print("=========================================")
    print()

    test_bounded_test_defaults()
    test_isolated_paths()
    test_explicit_paths_override_isolated_defaults()
    test_runner_uses_resolved_settings()

    print("CONTINUOUS RUNNER ENTRYPOINT: PASS")


if __name__ == "__main__":
    main()
