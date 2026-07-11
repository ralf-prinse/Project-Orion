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
        "trade_journal_path": None,
        "decision_journal_path": None,
        "runtime_event_path": None,
    }
    values.update(overrides)
    return Namespace(**values)


def test_isolated_paths():
    settings = resolve_settings(
        build_args(
            test=True,
            isolated=True,
        )
    )

    assert settings.session_path == Path(
        "data/optimization_trading_session.json"
    )
    assert settings.portfolio_path == Path(
        "data/optimization_paper_portfolio.json"
    )
    assert settings.trade_journal_path == Path(
        "data/optimization_trade_journal.jsonl"
    )
    assert settings.decision_journal_path == Path(
        "data/optimization_decision_journal.jsonl"
    )
    assert settings.runtime_event_path == Path(
        "data/optimization_runtime_events.jsonl"
    )


def test_runner_uses_journals_and_runtime_supervisor():
    settings = resolve_settings(
        build_args(
            test=True,
            isolated=True,
            iterations=1,
            interval=1,
            max_symbols=1,
        )
    )

    runner = build_runner(settings)
    autonomous_runner = runner.runner

    assert (
        autonomous_runner
        .trade_journal_repository
        .path
        == settings.trade_journal_path
    )
    assert (
        autonomous_runner
        .decision_journal_repository
        .path
        == settings.decision_journal_path
    )
    assert runner.supervisor is not None
    assert (
        runner.supervisor.event_repository.path
        == settings.runtime_event_path
    )


def main():
    print()
    print("=========================================")
    print("CONTINUOUS RUNNER ENTRYPOINT TEST")
    print("=========================================")
    print()

    test_isolated_paths()
    test_runner_uses_journals_and_runtime_supervisor()

    print(
        "CONTINUOUS RUNNER ENTRYPOINT: PASS"
    )


if __name__ == "__main__":
    main()
