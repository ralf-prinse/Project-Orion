from __future__ import annotations

import argparse
from dataclasses import dataclass

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Orion continuous paper trading with complete "
            "TradingSession persistence."
        ),
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help=(
            "Run a bounded smoke test. Defaults to 3 iterations, "
            "10 seconds and 5 symbols."
        ),
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help=(
            "Maximum number of continuous iterations. "
            "Omit for unlimited mode."
        ),
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help="Seconds between continuous iterations.",
    )
    parser.add_argument(
        "--max-symbols",
        type=int,
        default=None,
        help="Maximum number of market symbols scanned per iteration.",
    )
    parser.add_argument(
        "--initial-cash",
        type=float,
        default=500.0,
        help="Initial paper cash when no prior state exists.",
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
        raise ValueError("interval must be at least 1 second.")

    if max_iterations is not None and max_iterations < 1:
        raise ValueError("iterations must be at least 1.")

    if max_symbols < 1:
        raise ValueError("max-symbols must be at least 1.")

    if args.initial_cash <= 0:
        raise ValueError("initial-cash must be greater than zero.")

    return ContinuousRuntimeSettings(
        interval_seconds=interval_seconds,
        max_iterations=max_iterations,
        max_symbols=max_symbols,
        initial_cash=float(args.initial_cash),
        test_mode=bool(args.test),
    )


def build_runner(
    settings: ContinuousRuntimeSettings,
) -> ContinuousPaperTradingRunner:
    session_repository = JsonTradingSessionRepository(
        path="data/trading_session.json",
    )

    portfolio_repository = JsonPaperPortfolioRepository(
        path="data/paper_portfolio.json",
    )

    trade_journal_repository = JsonlTradeJournalRepository(
        path="data/trade_journal.jsonl",
    )

    autonomous_config = AutonomousPaperTradingConfig(
        cycles=1,
        sleep_seconds=0,
        live_config=LivePaperTradingConfig(
            initial_cash=settings.initial_cash,
            max_symbols=settings.max_symbols,
        ),
        print_cycle_summary=True,
    )

    autonomous_runner = AutonomousPaperTradingRunner(
        config=autonomous_config,
        trading_session_repository=session_repository,
        portfolio_repository=portfolio_repository,
        trade_journal_repository=trade_journal_repository,
    )

    continuous_config = ContinuousRunnerConfig(
        autonomous_config=autonomous_config,
        interval_seconds=settings.interval_seconds,
        max_iterations=settings.max_iterations,
        stop_on_exception=False,
        print_iteration_summary=True,
    )

    return ContinuousPaperTradingRunner(
        config=continuous_config,
        runner=autonomous_runner,
    )


def print_startup(
    settings: ContinuousRuntimeSettings,
) -> None:
    mode = "BOUNDED TEST" if settings.test_mode else "CONTINUOUS"

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
    print(f"Interval:         {settings.interval_seconds} seconds")
    print(f"Max symbols:      {settings.max_symbols}")
    print(f"Initial cash:     EUR {settings.initial_cash:.2f}")
    print("Session:          data/trading_session.json")
    print("Portfolio mirror: data/paper_portfolio.json")
    print("Trade journal:    data/trade_journal.jsonl")
    print("Press Ctrl+C to stop.")
    print("=========================================")
    print()


def print_result(result) -> None:
    print()
    print("=========================================")
    print("CONTINUOUS PAPER TRADING STOPPED")
    print("=========================================")
    print(f"Iterations completed: {result.iterations_completed}")
    print(f"Failed iterations:    {result.failed_iterations}")

    if result.last_result is not None:
        session = result.last_result.session

        print(f"Final cash:           EUR {result.last_result.final_cash:.2f}")
        print(f"Final equity:         EUR {result.last_result.final_equity:.2f}")
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
    parser = build_parser()
    args = parser.parse_args()
    settings = resolve_settings(args)

    print_startup(settings)

    runner = build_runner(settings)
    result = runner.run()

    print_result(result)


if __name__ == "__main__":
    main()
