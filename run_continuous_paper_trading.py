from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.continuous_runner_config import (
    ContinuousRunnerConfig,
)
from models.live_paper_trading_config import (
    LivePaperTradingConfig,
)
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)
from services.runtime_supervisor import RuntimeSupervisor
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)
from services.stores.jsonl_runtime_event_repository import (
    JsonlRuntimeEventRepository,
)
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)


@dataclass(frozen=True)
class ContinuousRuntimeSettings:
    interval_seconds: int
    max_iterations: int | None
    max_symbols: int
    initial_cash: float
    test_mode: bool
    stop_on_exception: bool
    session_path: Path
    portfolio_path: Path
    trade_journal_path: Path
    decision_journal_path: Path
    runtime_event_path: Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Orion continuous paper trading "
            "with complete session persistence."
        ),
    )

    parser.add_argument(
        "--test",
        action="store_true",
    )
    parser.add_argument(
        "--isolated",
        action="store_true",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--max-symbols",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--initial-cash",
        type=float,
        default=500.0,
    )
    parser.add_argument(
        "--stop-on-exception",
        action="store_true",
    )
    parser.add_argument(
        "--session-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--portfolio-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--trade-journal-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--decision-journal-path",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--runtime-event-path",
        type=Path,
        default=None,
    )

    return parser


def resolve_settings(
    args: argparse.Namespace,
) -> ContinuousRuntimeSettings:
    if args.test:
        interval_seconds = (
            args.interval
            if args.interval is not None
            else 10
        )
        max_iterations = (
            args.iterations
            if args.iterations is not None
            else 3
        )
        max_symbols = (
            args.max_symbols
            if args.max_symbols is not None
            else 5
        )
    else:
        interval_seconds = (
            args.interval
            if args.interval is not None
            else 300
        )
        max_iterations = args.iterations
        max_symbols = (
            args.max_symbols
            if args.max_symbols is not None
            else 25
        )

    if interval_seconds < 1:
        raise ValueError(
            "interval must be at least 1 second."
        )

    if (
        max_iterations is not None
        and max_iterations < 1
    ):
        raise ValueError(
            "iterations must be at least 1."
        )

    if max_symbols < 1:
        raise ValueError(
            "max-symbols must be at least 1."
        )

    if args.initial_cash <= 0:
        raise ValueError(
            "initial-cash must be greater than zero."
        )

    session_path = Path(
        "data/trading_session.json"
    )
    portfolio_path = Path(
        "data/paper_portfolio.json"
    )
    trade_journal_path = Path(
        "data/trade_journal.jsonl"
    )
    decision_journal_path = Path(
        "data/decision_journal.jsonl"
    )
    runtime_event_path = Path(
        "data/runtime_events.jsonl"
    )

    if args.isolated:
        session_path = Path(
            "data/optimization_trading_session.json"
        )
        portfolio_path = Path(
            "data/optimization_paper_portfolio.json"
        )
        trade_journal_path = Path(
            "data/optimization_trade_journal.jsonl"
        )
        decision_journal_path = Path(
            "data/optimization_decision_journal.jsonl"
        )
        runtime_event_path = Path(
            "data/optimization_runtime_events.jsonl"
        )

    return ContinuousRuntimeSettings(
        interval_seconds=interval_seconds,
        max_iterations=max_iterations,
        max_symbols=max_symbols,
        initial_cash=float(args.initial_cash),
        test_mode=bool(args.test),
        stop_on_exception=bool(
            args.stop_on_exception
        ),
        session_path=(
            args.session_path
            or session_path
        ),
        portfolio_path=(
            args.portfolio_path
            or portfolio_path
        ),
        trade_journal_path=(
            args.trade_journal_path
            or trade_journal_path
        ),
        decision_journal_path=(
            args.decision_journal_path
            or decision_journal_path
        ),
        runtime_event_path=(
            args.runtime_event_path
            or runtime_event_path
        ),
    )


def build_runner(
    settings: ContinuousRuntimeSettings,
) -> ContinuousPaperTradingRunner:
    autonomous_config = (
        AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
            live_config=LivePaperTradingConfig(
                initial_cash=settings.initial_cash,
                max_symbols=settings.max_symbols,
            ),
            print_cycle_summary=True,
        )
    )

    autonomous_runner = (
        AutonomousPaperTradingRunner(
            config=autonomous_config,
            trading_session_repository=(
                JsonTradingSessionRepository(
                    path=settings.session_path,
                )
            ),
            portfolio_repository=(
                JsonPaperPortfolioRepository(
                    path=settings.portfolio_path,
                )
            ),
            trade_journal_repository=(
                JsonlTradeJournalRepository(
                    path=settings.trade_journal_path,
                )
            ),
            decision_journal_repository=(
                JsonlTradeJournalRepository(
                    path=settings.decision_journal_path,
                )
            ),
        )
    )

    return ContinuousPaperTradingRunner(
        config=ContinuousRunnerConfig(
            autonomous_config=autonomous_config,
            interval_seconds=(
                settings.interval_seconds
            ),
            max_iterations=settings.max_iterations,
            stop_on_exception=(
                settings.stop_on_exception
            ),
            print_iteration_summary=True,
        ),
        runner=autonomous_runner,
        supervisor=RuntimeSupervisor(
            event_repository=JsonlRuntimeEventRepository(
                path=settings.runtime_event_path,
            )
        ),
    )


def print_startup(
    settings: ContinuousRuntimeSettings,
) -> None:
    mode = (
        "BOUNDED TEST"
        if settings.test_mode
        else "CONTINUOUS"
    )
    iterations = (
        str(settings.max_iterations)
        if settings.max_iterations is not None
        else "unlimited"
    )

    print()
    print("=========================================")
    print("ORION CONTINUOUS PAPER TRADING")
    print("=========================================")
    print(f"Mode:             {mode}")
    print(f"Iterations:       {iterations}")
    print(
        "Interval:         "
        f"{settings.interval_seconds} seconds"
    )
    print(
        f"Max symbols:      {settings.max_symbols}"
    )
    print(
        "Initial cash:     "
        f"EUR {settings.initial_cash:.2f}"
    )
    print(
        "Stop on failure:  "
        f"{settings.stop_on_exception}"
    )
    print(f"Session:          {settings.session_path}")
    print(
        "Portfolio mirror: "
        f"{settings.portfolio_path}"
    )
    print(
        "Trade journal:    "
        f"{settings.trade_journal_path}"
    )
    print(
        "Decision journal: "
        f"{settings.decision_journal_path}"
    )
    print(
        "Runtime events:   "
        f"{settings.runtime_event_path}"
    )
    print("Press Ctrl+C to stop.")
    print("=========================================")
    print()


def print_result(result) -> None:
    print()
    print("=========================================")
    print("CONTINUOUS PAPER TRADING STOPPED")
    print("=========================================")
    print(
        "Iterations completed: "
        f"{result.iterations_completed}"
    )
    print(
        "Failed iterations:    "
        f"{result.failed_iterations}"
    )

    if result.last_result is not None:
        session = result.last_result.session

        print(
            "Final cash:           "
            f"EUR {result.last_result.final_cash:.2f}"
        )
        print(
            "Final equity:         "
            f"EUR {result.last_result.final_equity:.2f}"
        )
        print(
            "Open positions:       "
            f"{len(session.portfolio.positions)}"
        )
        print(
            "Position states:      "
            f"{len(session.position_states)}"
        )
        print(
            "Risk plans:           "
            f"{len(session.risk_plans)}"
        )

    print("=========================================")
    print()


def main() -> None:
    args = build_parser().parse_args()
    settings = resolve_settings(args)
    print_startup(settings)

    runner = build_runner(settings)
    result = runner.run()

    print_result(result)


if __name__ == "__main__":
    main()
