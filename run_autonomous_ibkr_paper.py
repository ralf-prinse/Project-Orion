from __future__ import annotations

import os

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import (
    LivePaperTradingConfig,
)
from services.ibkr.ibkr_autonomous_runtime_factory import (
    IbkrAutonomousRuntimeFactory,
)
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)
from services.stores.json_paper_portfolio_repository import (
    JsonPaperPortfolioRepository,
)
from services.stores.json_trading_session_repository import (
    JsonTradingSessionRepository,
)
from models.position_adoption import PositionAdoptionConfig
from services.position_adoption_service import PositionAdoptionService


ACCOUNT_ENVIRONMENT_VARIABLE = "ORION_IBKR_PAPER_ACCOUNT_ID"
ORDER_PERMISSION_ENVIRONMENT_VARIABLE = "ORION_IBKR_ALLOW_ORDERS"
EXECUTION_MODE_ENVIRONMENT_VARIABLE = "ORION_IBKR_EXECUTION_MODE"
CYCLES_ENVIRONMENT_VARIABLE = "ORION_IBKR_CYCLES"
SCAN_INTERVAL_ENVIRONMENT_VARIABLE = "ORION_IBKR_SCAN_INTERVAL_SECONDS"
EXIT_STRATEGY_ENVIRONMENT_VARIABLE = "ORION_IBKR_EXIT_STRATEGY"
PRICING_PLAN_ENVIRONMENT_VARIABLE = "ORION_IBKR_PRICING_PLAN"

DEFAULT_CYCLES = 1
DEFAULT_SCAN_INTERVAL_SECONDS = 900
MAX_CYCLES = 96
MIN_SCAN_INTERVAL_SECONDS = 60
MAX_SCAN_INTERVAL_SECONDS = 3600

EXIT_ONLY_CONFIRMATION = "START EXIT ONLY IBKR PAPER CYCLE"
BUY_AND_SELL_CONFIRMATION = "START ONE AUTONOMOUS IBKR PAPER CYCLE"


def read_required_paper_account_id() -> str:
    account_id = os.getenv(
        ACCOUNT_ENVIRONMENT_VARIABLE,
        "",
    ).strip().upper()

    if not account_id:
        raise RuntimeError(
            "IBKR Paper account ID is not configured. "
            f"Set {ACCOUNT_ENVIRONMENT_VARIABLE} to your "
            "Paper account ID beginning with 'DU'."
        )

    if not account_id.startswith("DU"):
        raise RuntimeError(
            f"{ACCOUNT_ENVIRONMENT_VARIABLE} must contain an "
            "IBKR Paper account ID beginning with 'DU'."
        )

    return account_id


def order_submission_is_enabled() -> bool:
    value = os.getenv(
        ORDER_PERMISSION_ENVIRONMENT_VARIABLE,
        "",
    ).strip().lower()

    return value == "true"


def read_execution_mode() -> str:
    value = os.getenv(
        EXECUTION_MODE_ENVIRONMENT_VARIABLE,
        AutonomousPaperTradingConfig.EXIT_ONLY,
    ).strip().upper()

    if value not in {
        AutonomousPaperTradingConfig.EXIT_ONLY,
        AutonomousPaperTradingConfig.BUY_AND_SELL,
    }:
        raise RuntimeError(
            f"{EXECUTION_MODE_ENVIRONMENT_VARIABLE} must be "
            "EXIT_ONLY or BUY_AND_SELL."
        )

    return value


def _read_bounded_integer(
    *,
    environment_variable: str,
    default: int,
    minimum: int,
    maximum: int,
) -> int:
    raw_value = os.getenv(
        environment_variable,
        str(default),
    ).strip()

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(
            f"{environment_variable} must be a whole number."
        ) from exc

    if not minimum <= value <= maximum:
        raise RuntimeError(
            f"{environment_variable} must be between "
            f"{minimum} and {maximum}."
        )

    return value


def read_cycle_count() -> int:
    return _read_bounded_integer(
        environment_variable=CYCLES_ENVIRONMENT_VARIABLE,
        default=DEFAULT_CYCLES,
        minimum=1,
        maximum=MAX_CYCLES,
    )


def read_scan_interval_seconds() -> int:
    return _read_bounded_integer(
        environment_variable=SCAN_INTERVAL_ENVIRONMENT_VARIABLE,
        default=DEFAULT_SCAN_INTERVAL_SECONDS,
        minimum=MIN_SCAN_INTERVAL_SECONDS,
        maximum=MAX_SCAN_INTERVAL_SECONDS,
    )


def read_exit_strategy() -> str:
    value = os.getenv(
        EXIT_STRATEGY_ENVIRONMENT_VARIABLE,
        LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT,
    ).strip().upper()
    if value not in {
        LivePaperTradingConfig.SWING,
        LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT,
    }:
        raise RuntimeError(
            f"{EXIT_STRATEGY_ENVIRONMENT_VARIABLE} must be "
            "SWING or COST_AWARE_SMALL_PROFIT."
        )
    return value


def read_pricing_plan() -> str:
    value = os.getenv(
        PRICING_PLAN_ENVIRONMENT_VARIABLE,
        LivePaperTradingConfig.FIXED_PRICING,
    ).strip().upper()
    if value not in {
        LivePaperTradingConfig.FIXED_PRICING,
        LivePaperTradingConfig.TIERED_PRICING,
    }:
        raise RuntimeError(
            f"{PRICING_PLAN_ENVIRONMENT_VARIABLE} must be "
            "FIXED or TIERED."
        )
    return value


def build_config(
    execution_mode: str = AutonomousPaperTradingConfig.EXIT_ONLY,
    cycles: int = DEFAULT_CYCLES,
    scan_interval_seconds: int = DEFAULT_SCAN_INTERVAL_SECONDS,
    exit_strategy: str = (
        LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT
    ),
    pricing_plan: str = LivePaperTradingConfig.FIXED_PRICING,
) -> AutonomousPaperTradingConfig:
    live_config = LivePaperTradingConfig(
        watchlist_path="data/universes/ibkr_eu_us_validation.csv",
        initial_cash=10_000.0,
        max_symbols=100,
        max_open_positions=20,
        min_confidence=0.75,
        max_position_value=1000.0,
        max_position_size_pct=0.10,
        exit_strategy=exit_strategy,
        ibkr_pricing_plan=pricing_plan,
    )

    return AutonomousPaperTradingConfig(
        live_config=live_config,
        execution_mode=execution_mode,
        cycles=cycles,
        sleep_seconds=float(scan_interval_seconds),
        stop_on_exception=True,
        print_cycle_summary=True,
    )


def mask_account_id(account_id: str) -> str:
    if len(account_id) <= 4:
        return "****"

    return f"{account_id[:2]}*****{account_id[-2:]}"


def print_runtime_mode(
    *,
    paper_account_id: str,
    allow_order_submission: bool,
    execution_mode: str,
    config: AutonomousPaperTradingConfig,
) -> None:
    print()
    print("=========================================")
    print("ORION AUTONOMOUS IBKR PAPER TRADING")
    print("=========================================")
    print(f"Account:           {mask_account_id(paper_account_id)}")
    print("TWS host:          127.0.0.1")
    print("TWS Paper port:    7497")
    print("Base currency:     EUR (required)")
    print(f"Cycles:            {config.cycles}")
    print(
        "Scan interval:     "
        f"{config.sleep_seconds:g} seconds"
    )
    print("Maximum symbols:   100 (50 US + 50 EU)")
    print("Maximum positions: 20 (risk-limited ceiling)")
    print(f"Execution mode:    {execution_mode}")
    print(
        "Exit strategy:     "
        f"{config.live_config.exit_strategy}"
    )
    print(
        "IBKR pricing:      "
        f"{config.live_config.ibkr_pricing_plan}"
    )
    if (
        config.live_config.exit_strategy
        == LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT
    ):
        print(
            "Net profit goals: US EUR "
            f"{config.live_config.small_profit_target_us_eur:.2f}"
            " / EU EUR "
            f"{config.live_config.small_profit_target_eu_eur:.2f}"
        )
        print(
            "Net loss limits:  US EUR -"
            f"{config.live_config.small_profit_max_loss_us_eur:.2f}"
            " / EU EUR -"
            f"{config.live_config.small_profit_max_loss_eu_eur:.2f}"
        )
    print(
        "Order submission: "
        + (
            "ENABLED"
            if allow_order_submission
            else "DISABLED"
        )
    )
    print(
        "BUY execution:     "
        + (
            "DISABLED"
            if not allow_order_submission
            else (
                "BLOCKED BY EXIT_ONLY"
                if execution_mode == AutonomousPaperTradingConfig.EXIT_ONLY
                else "IBKR"
            )
        )
    )
    print(
        "SELL execution:    "
        + (
            "IBKR"
            if allow_order_submission
            else "DISABLED"
        )
    )
    print("Broker sync:       ENABLED")
    print("Adopt positions:   AAPL, AAL, ASML.AS, ASM.AS")
    print("=========================================")
    print()

    if not allow_order_submission:
        print(
            "SAFE MODE: Orion can connect to TWS and synchronize "
            "the Paper account, but IBKR order submission is disabled."
        )
        print()


def require_confirmation(execution_mode: str, cycles: int = 1) -> bool:
    if cycles == 1:
        confirmation = (
            EXIT_ONLY_CONFIRMATION
            if execution_mode == AutonomousPaperTradingConfig.EXIT_ONLY
            else BUY_AND_SELL_CONFIRMATION
        )
    elif execution_mode == AutonomousPaperTradingConfig.EXIT_ONLY:
        confirmation = (
            f"START {cycles} EXIT ONLY IBKR PAPER CYCLES"
        )
    else:
        confirmation = (
            f"START {cycles} AUTONOMOUS IBKR PAPER CYCLES"
        )
    typed = input(
        f"Type exactly '{confirmation}' to continue: "
    ).strip()

    if typed != confirmation:
        print("Confirmation mismatch. No runner was started.")
        return False

    return True


def print_result(result) -> None:
    print()
    print("=========================================")
    print("AUTONOMOUS IBKR PAPER RESULT")
    print("=========================================")
    print(f"Completed cycles: {result.completed_cycles}")
    print(f"Failed cycles:    {result.failed_cycles}")
    print(f"Scanned symbols:  {result.total_scanned_symbols}")
    print(f"Analyzed symbols: {result.total_analyzed_symbols}")
    print(f"Skipped/failed:   {result.total_failed_symbols}")
    print(f"Executed trades:  {result.total_executed_trades}")
    print(f"Executed exits:   {result.total_executed_exits}")
    print(f"Rejected trades:  {result.total_rejected_trades}")
    print(
        "Allocation rejects: "
        f"{result.total_allocation_rejections}"
    )
    print(
        "Execution rejects:  "
        f"{result.total_execution_rejections}"
    )
    print(f"Risk evaluations: {result.risk_evaluations}")
    print(f"Risk rejections:  {result.risk_rejections}")
    print(f"Final cash:       {result.final_cash:.2f}")
    print(f"Final equity:     {result.final_equity:.2f}")
    print(f"Open positions:   {result.session.open_positions}")
    print("=========================================")
    print()


def main() -> None:
    paper_account_id = read_required_paper_account_id()
    allow_order_submission = order_submission_is_enabled()
    execution_mode = read_execution_mode()
    cycles = read_cycle_count()
    scan_interval_seconds = read_scan_interval_seconds()
    exit_strategy = read_exit_strategy()
    pricing_plan = read_pricing_plan()
    config = build_config(
        execution_mode=execution_mode,
        cycles=cycles,
        scan_interval_seconds=scan_interval_seconds,
        exit_strategy=exit_strategy,
        pricing_plan=pricing_plan,
    )

    print_runtime_mode(
        paper_account_id=paper_account_id,
        allow_order_submission=allow_order_submission,
        execution_mode=execution_mode,
        config=config,
    )

    if not require_confirmation(execution_mode, cycles):
        return

    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id=paper_account_id,
        config=config,
        trade_journal_repository=JsonlTradeJournalRepository(
            path="data/ibkr_autonomous_trade_journal.jsonl",
        ),
        decision_journal_repository=JsonlTradeJournalRepository(
            path="data/ibkr_autonomous_decision_journal.jsonl",
        ),
        trading_session_repository=JsonTradingSessionRepository(
            path="data/ibkr_autonomous_trading_session.json",
        ),
        portfolio_repository=JsonPaperPortfolioRepository(
            path="data/ibkr_autonomous_paper_portfolio.json",
        ),
        position_adoption_service=PositionAdoptionService(
            PositionAdoptionConfig(
                allowed_symbols=(
                    "AAPL",
                    "AAL",
                    "ASML.AS",
                    "ASM.AS",
                ),
            )
        ),
        allow_order_submission=allow_order_submission,
    )

    result = runtime.runner.run()

    print_result(result)


if __name__ == "__main__":
    main()
