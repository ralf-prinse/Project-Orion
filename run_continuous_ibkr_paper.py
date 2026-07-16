from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.continuous_runner_config import ContinuousRunnerConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from providers.yahoo_provider import YahooProvider
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.continuous_paper_trading_runner import (
    ContinuousPaperTradingRunner,
)
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_broker import IbkrBroker
from services.ibkr.ibkr_order_transport import IbkrOrderTransport
from services.ibkr.ibkr_trading_session_sync_service import (
    IbkrTradingSessionSyncService,
)
from services.market_session_service import MarketSessionService
from services.paper_trading_service import PaperTradingService
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
from services.trading_cycle import TradingCycle


CONFIRMATION = "START CONTINUOUS IBKR PAPER VALIDATION"


@dataclass(frozen=True)
class DisabledExitResult:
    executed: bool = False


class BuyOnlyExitEngine:
    """
    Prevents local-only exit execution.

    Real IBKR SELL execution is not enabled yet.
    """

    def execute(self, *, portfolio, decision) -> DisabledExitResult:
        return DisabledExitResult()


def require_account_id() -> str:
    account_id = (
        os.environ
        .get("ORION_IBKR_PAPER_ACCOUNT_ID", "")
        .strip()
        .upper()
    )

    if not account_id.startswith("DU"):
        raise RuntimeError(
            "Set ORION_IBKR_PAPER_ACCOUNT_ID to the "
            "DU-prefixed TWS Paper account."
        )

    return account_id


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run a bounded continuous Orion validation "
            "against IBKR TWS Paper."
        )
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--max-symbols",
        type=int,
        default=25,
    )
    parser.add_argument(
        "--max-open-positions",
        type=int,
        default=3,
    )
    parser.add_argument(
        "--watchlist",
        type=Path,
        default=Path(
            "data/universes/ibkr_us_validation.csv"
        ),
    )
    parser.add_argument(
        "--ignore-market-hours",
        action="store_true",
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    if args.iterations < 1:
        raise ValueError("iterations must be at least 1.")

    if args.interval < 1:
        raise ValueError("interval must be at least 1 second.")

    if args.max_symbols < 1:
        raise ValueError("max-symbols must be at least 1.")

    if args.max_open_positions < 1:
        raise ValueError(
            "max-open-positions must be at least 1."
        )

    if not args.watchlist.exists():
        raise FileNotFoundError(
            f"Watchlist does not exist: {args.watchlist}"
        )


def build_runner(
    *,
    account_id: str,
    args: argparse.Namespace,
) -> ContinuousPaperTradingRunner:
    price_provider = YahooProvider()

    account_service = IbkrAccountService(
        host="127.0.0.1",
        port=7497,
        client_id=110,
        timeout_seconds=15.0,
        expected_account_id=account_id,
    )

    sync_service = IbkrTradingSessionSyncService(
        account_service=account_service,
        price_provider=price_provider,
    )

    transport = IbkrOrderTransport(
        paper_account_id=account_id,
        host="127.0.0.1",
        port=7497,
        client_id=141,
        connection_timeout_seconds=15.0,
        reconciliation_timeout_seconds=5.0,
        reconciliation_attempts=3,
        reconciliation_retry_delay_seconds=0.25,
        allow_order_submission=True,
        disconnect_after_order=True,
    )

    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=45.0,
        exchange="SMART",
        currency="USD",
    )

    execution_engine = ExecutionEngine(
        broker=broker,
    )

    paper_trading_service = PaperTradingService(
        execution_engine=execution_engine,
    )

    trading_cycle = TradingCycle(
        paper_trading_service=paper_trading_service,
    )

    live_config = LivePaperTradingConfig(
        watchlist_path=args.watchlist,
        initial_cash=1.0,
        max_symbols=args.max_symbols,
        max_open_positions=args.max_open_positions,
        min_confidence=0.75,
        max_position_value=150.0,
    )

    autonomous_config = AutonomousPaperTradingConfig(
        live_config=live_config,
        cycles=1,
        sleep_seconds=0.0,
        stop_on_exception=True,
        print_cycle_summary=True,
    )

    autonomous_runner = AutonomousPaperTradingRunner(
        config=autonomous_config,
        trading_cycle=trading_cycle,
        trading_session_repository=(
            JsonTradingSessionRepository(
                path=Path(
                    "data/ibkr_trading_session.json"
                )
            )
        ),
        portfolio_repository=(
            JsonPaperPortfolioRepository(
                path=Path(
                    "data/ibkr_paper_portfolio.json"
                )
            )
        ),
        trade_journal_repository=(
            JsonlTradeJournalRepository(
                path=Path(
                    "data/ibkr_trade_journal.jsonl"
                )
            )
        ),
        decision_journal_repository=(
            JsonlTradeJournalRepository(
                path=Path(
                    "data/ibkr_decision_journal.jsonl"
                )
            )
        ),
        price_provider=price_provider,
        exit_engine=BuyOnlyExitEngine(),
        trading_session_sync_service=sync_service,
    )

    return ContinuousPaperTradingRunner(
        config=ContinuousRunnerConfig(
            autonomous_config=autonomous_config,
            interval_seconds=args.interval,
            max_iterations=args.iterations,
            stop_on_exception=True,
            print_iteration_summary=True,
        ),
        runner=autonomous_runner,
        supervisor=RuntimeSupervisor(
            event_repository=JsonlRuntimeEventRepository(
                path=Path(
                    "data/ibkr_runtime_events.jsonl"
                )
            )
        ),
        market_session_service=(
            None
            if args.ignore_market_hours
            else MarketSessionService()
        ),
    )


def print_startup(
    *,
    account_id: str,
    args: argparse.Namespace,
) -> None:
    print()
    print("=========================================")
    print("ORION CONTINUOUS IBKR PAPER VALIDATION")
    print("=========================================")
    print(
        f"Account:            "
        f"{account_id[:2]}*****{account_id[-2:]}"
    )
    print("TWS host:           127.0.0.1")
    print("TWS Paper port:     7497")
    print(f"Iterations:         {args.iterations}")
    print(f"Interval:           {args.interval} seconds")
    print(f"Max symbols:        {args.max_symbols}")
    print(
        f"Max open positions: "
        f"{args.max_open_positions}"
    )
    print(f"Watchlist:          {args.watchlist}")
    print("Broker orders:      BUY enabled")
    print("Broker exits:       DISABLED")
    print("Stop on failure:    YES")
    print("Automatic retry:    NO")
    print("=========================================")
    print()


def print_result(result) -> None:
    print()
    print("=========================================")
    print("IBKR VALIDATION STOPPED")
    print("=========================================")
    print(
        f"Iterations completed: "
        f"{result.iterations_completed}"
    )
    print(
        f"Failed iterations:    "
        f"{result.failed_iterations}"
    )
    print(
        f"Idle iterations:      "
        f"{result.idle_iterations}"
    )

    if result.last_result is not None:
        session = result.last_result.session

        print(
            f"Final cash:           "
            f"{result.last_result.final_cash:.2f}"
        )
        print(
            f"Final equity:         "
            f"{result.last_result.final_equity:.2f}"
        )
        print(
            f"Open positions:       "
            f"{session.open_positions}"
        )

    print("=========================================")
    print()


def main() -> None:
    args = build_parser().parse_args()
    validate_args(args)

    account_id = require_account_id()
    print_startup(
        account_id=account_id,
        args=args,
    )

    typed = input(
        f"Type exactly '{CONFIRMATION}' to continue: "
    ).strip()

    if typed != CONFIRMATION:
        print(
            "Confirmation mismatch. "
            "No continuous runtime was started."
        )
        return

    runner = build_runner(
        account_id=account_id,
        args=args,
    )

    result = runner.run()
    print_result(result)


if __name__ == "__main__":
    main()