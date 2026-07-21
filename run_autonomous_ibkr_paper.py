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
from services.stores.jsonl_news_event_repository import (
    JsonlNewsEventRepository,
)
from services.stores.jsonl_news_assessment_repository import (
    JsonlNewsAssessmentRepository,
)
from services.stores.jsonl_completed_trade_repository import (
    JsonlCompletedTradeRepository,
)


ACCOUNT_ENVIRONMENT_VARIABLE = "ORION_IBKR_PAPER_ACCOUNT_ID"
ORDER_PERMISSION_ENVIRONMENT_VARIABLE = "ORION_IBKR_ALLOW_ORDERS"
EXECUTION_MODE_ENVIRONMENT_VARIABLE = "ORION_IBKR_EXECUTION_MODE"
CYCLES_ENVIRONMENT_VARIABLE = "ORION_IBKR_CYCLES"
SCAN_INTERVAL_ENVIRONMENT_VARIABLE = "ORION_IBKR_SCAN_INTERVAL_SECONDS"
EXIT_STRATEGY_ENVIRONMENT_VARIABLE = "ORION_IBKR_EXIT_STRATEGY"
PRICING_PLAN_ENVIRONMENT_VARIABLE = "ORION_IBKR_PRICING_PLAN"
NEWS_MODE_ENVIRONMENT_VARIABLE = "ORION_IBKR_NEWS_MODE"
CAPITAL_PROFILE_ENVIRONMENT_VARIABLE = "ORION_CAPITAL_PROFILE"
MARKET_DATA_COST_ENVIRONMENT_VARIABLE = (
    "ORION_MONTHLY_MARKET_DATA_COST_EUR"
)

DEFAULT_CYCLES = 1
DEFAULT_SCAN_INTERVAL_SECONDS = 900
MAX_CYCLES = 96
MIN_SCAN_INTERVAL_SECONDS = 60
MAX_SCAN_INTERVAL_SECONDS = 3600

EXIT_ONLY_CONFIRMATION = "START EXIT ONLY IBKR PAPER CYCLE"
BUY_AND_SELL_CONFIRMATION = "START ONE AUTONOMOUS IBKR PAPER CYCLE"
SHADOW_CONFIRMATION = "START ONE ORION SHADOW CYCLE"
MICRO_500_SHADOW_CONFIRMATION = (
    "START ONE ORION MICRO 500 SHADOW CYCLE"
)


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
        AutonomousPaperTradingConfig.SHADOW,
    }:
        raise RuntimeError(
            f"{EXECUTION_MODE_ENVIRONMENT_VARIABLE} must be "
            "EXIT_ONLY, BUY_AND_SELL, or SHADOW."
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


def read_pricing_plan(
    default: str = LivePaperTradingConfig.FIXED_PRICING,
) -> str:
    value = os.getenv(
        PRICING_PLAN_ENVIRONMENT_VARIABLE,
        default,
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


def read_capital_profile() -> str:
    value = os.getenv(
        CAPITAL_PROFILE_ENVIRONMENT_VARIABLE,
        LivePaperTradingConfig.STANDARD_10000,
    ).strip().upper()
    if value not in {
        LivePaperTradingConfig.STANDARD_10000,
        LivePaperTradingConfig.MICRO_500,
    }:
        raise RuntimeError(
            f"{CAPITAL_PROFILE_ENVIRONMENT_VARIABLE} must be "
            "STANDARD_10000 or MICRO_500."
        )
    return value


def read_monthly_market_data_cost_eur(*, default: float) -> float:
    raw_value = os.getenv(
        MARKET_DATA_COST_ENVIRONMENT_VARIABLE,
        str(default),
    ).strip()
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise RuntimeError(
            f"{MARKET_DATA_COST_ENVIRONMENT_VARIABLE} must be a number."
        ) from exc
    if value < 0 or value > 1000:
        raise RuntimeError(
            f"{MARKET_DATA_COST_ENVIRONMENT_VARIABLE} must be between "
            "zero and 1000."
        )
    return value


def read_news_mode() -> str:
    value = os.getenv(
        NEWS_MODE_ENVIRONMENT_VARIABLE,
        LivePaperTradingConfig.NEWS_SHADOW,
    ).strip().upper()
    if value not in {
        LivePaperTradingConfig.NEWS_DISABLED,
        LivePaperTradingConfig.NEWS_SHADOW,
    }:
        raise RuntimeError(
            f"{NEWS_MODE_ENVIRONMENT_VARIABLE} must be "
            "DISABLED or SHADOW."
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
    news_mode: str = LivePaperTradingConfig.NEWS_SHADOW,
    capital_profile: str = LivePaperTradingConfig.STANDARD_10000,
    monthly_market_data_cost_eur: float = 0.0,
) -> AutonomousPaperTradingConfig:
    capital_profile = capital_profile.strip().upper()
    shared = dict(
        watchlist_path="data/universes/ibkr_eu_us_validation.csv",
        max_symbols=100,
        min_confidence=0.75,
        exit_strategy=exit_strategy,
        ibkr_pricing_plan=pricing_plan,
        news_mode=news_mode,
        enable_execution_quality_gate=(
            execution_mode != AutonomousPaperTradingConfig.SHADOW
        ),
        enable_native_protective_orders=(
            execution_mode != AutonomousPaperTradingConfig.SHADOW
        ),
    )
    if capital_profile == LivePaperTradingConfig.MICRO_500:
        live_config = LivePaperTradingConfig(
            **shared,
            capital_profile=capital_profile,
            initial_cash=500.0,
            max_open_positions=2,
            max_new_positions_per_cycle=1,
            max_new_positions_per_day=2,
            reentry_cooldown_minutes=60,
            max_position_value=175.0,
            max_position_size_pct=0.35,
            max_portfolio_exposure=0.70,
            min_cash_reserve_pct=0.30,
            max_risk_per_trade_pct=0.01,
            max_portfolio_risk_pct=0.02,
            max_drawdown_pct=0.05,
            history_period="5d",
            history_interval="5m",
            max_history_age_minutes=10,
            max_holding_minutes=90,
            small_profit_target_us_eur=2.5,
            small_profit_target_eu_eur=3.5,
            small_profit_max_loss_us_eur=3.0,
            small_profit_max_loss_eu_eur=4.0,
            estimated_monthly_market_data_cost_eur=(
                monthly_market_data_cost_eur
            ),
            expected_monthly_round_trips=40,
            max_round_trip_cost_pct=0.02,
            max_required_gross_move_pct=0.03,
            entry_cost_uncertainty_buffer_eur=0.50,
            max_daily_loss_pct=0.015,
            max_positions_per_market=2,
            max_market_exposure_pct=0.70,
            max_positions_per_sector=1,
            max_sector_exposure_pct=0.35,
            max_positions_per_correlation_cluster=1,
        )
    else:
        live_config = LivePaperTradingConfig(
            **shared,
            capital_profile=capital_profile,
            initial_cash=10_000.0,
            max_open_positions=20,
            max_position_value=1000.0,
            max_position_size_pct=0.10,
            estimated_monthly_market_data_cost_eur=(
                monthly_market_data_cost_eur
            ),
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


def build_storage_prefix(
    *,
    execution_mode: str,
    capital_profile: str,
) -> str:
    capital_profile = capital_profile.strip().upper()
    if execution_mode != AutonomousPaperTradingConfig.SHADOW:
        return "data/ibkr_autonomous"
    if capital_profile == LivePaperTradingConfig.MICRO_500:
        return "data/orion_shadow_micro_500"
    return "data/orion_shadow"


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
    print(
        "Capital profile:   "
        f"{config.live_config.capital_profile}"
    )
    print(
        "Starting capital:  EUR "
        f"{config.live_config.initial_cash:.2f}"
    )
    print(f"Cycles:            {config.cycles}")
    print(
        "Scan interval:     "
        f"{config.sleep_seconds:g} seconds"
    )
    print("Maximum symbols:   100 (50 US + 50 EU)")
    print(
        "Market candles:    "
        f"{config.live_config.history_period} / "
        f"{config.live_config.history_interval}"
    )
    if config.live_config.max_history_age_minutes is not None:
        print(
            "Candle freshness: max "
            f"{config.live_config.max_history_age_minutes} minutes"
        )
    print(
        "Maximum positions: "
        f"{config.live_config.max_open_positions} "
        "(risk-limited ceiling)"
    )
    print(
        "Daily entry limit: "
        f"{config.live_config.max_new_positions_per_day}"
    )
    print(
        "Maximum position:  EUR "
        f"{config.live_config.max_position_value:.2f}"
    )
    print(f"Execution mode:    {execution_mode}")
    print(
        "Exit strategy:     "
        f"{config.live_config.exit_strategy}"
    )
    print(
        "IBKR pricing:      "
        f"{config.live_config.ibkr_pricing_plan}"
    )
    print(
        "Market data budget: EUR "
        f"{config.live_config.estimated_monthly_market_data_cost_eur:.2f}"
        "/month"
    )
    print(
        "News intelligence: "
        f"{config.live_config.news_mode} (never changes orders)"
    )
    print(
        "Execution quotes:  "
        + (
            "YAHOO REFERENCE + COST/SLIPPAGE BUFFER"
            if execution_mode == AutonomousPaperTradingConfig.SHADOW
            else (
                "IBKR LIVE BID/ASK (fail-closed)"
                if config.live_config.enable_execution_quality_gate
                else "DISABLED"
            )
        )
    )
    print(
        "Native protection: "
        + (
            "SIMULATED POSITION LIFECYCLE"
            if execution_mode == AutonomousPaperTradingConfig.SHADOW
            else (
                "IBKR BRACKET + OCA"
                if config.live_config.enable_native_protective_orders
                else "DISABLED"
            )
        )
    )
    print(
        "Session breaker:   "
        f"{config.live_config.max_daily_loss_pct:.1%} loss / "
        f"{config.live_config.max_consecutive_losses} losses / "
        f"{config.live_config.max_consecutive_order_failures} order failures"
    )
    print(
        "Concentration:     "
        f"max {config.live_config.max_positions_per_sector} per sector / "
        f"{config.live_config.max_sector_exposure_pct:.0%} exposure"
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
        if config.live_config.max_holding_minutes is not None:
            print(
                "Maximum hold:      "
                f"{config.live_config.max_holding_minutes} minutes"
            )
        print(
            "Economic entry:   max costs "
            f"{config.live_config.max_round_trip_cost_pct:.1%} / "
            "required move "
            f"{config.live_config.max_required_gross_move_pct:.1%}"
        )
    print(
        "Order submission: "
        + (
            "PERMANENTLY BLOCKED BY SHADOW"
            if execution_mode == AutonomousPaperTradingConfig.SHADOW
            else ("ENABLED" if allow_order_submission else "DISABLED")
        )
    )
    print(
        "BUY execution:     "
        + (
            "SHADOW SIMULATION"
            if execution_mode == AutonomousPaperTradingConfig.SHADOW
            else (
                "DISABLED"
                if not allow_order_submission
                else (
                "BLOCKED BY EXIT_ONLY"
                if execution_mode == AutonomousPaperTradingConfig.EXIT_ONLY
                else "IBKR"
                )
            )
        )
    )
    print(
        "SELL execution:    "
        + (
            "SHADOW SIMULATION"
            if execution_mode == AutonomousPaperTradingConfig.SHADOW
            else ("IBKR" if allow_order_submission else "DISABLED")
        )
    )
    if execution_mode == AutonomousPaperTradingConfig.SHADOW:
        print("Broker sync:       DISABLED (isolated shadow portfolio)")
        print("Adopt positions:   DISABLED")
    else:
        print("Broker sync:       ENABLED")
        print("Adopt positions:   AAPL, AAL, ASML.AS, ASM.AS")
    print("=========================================")
    print()

    if execution_mode == AutonomousPaperTradingConfig.SHADOW:
        print(
            "SHADOW MODE: Orion uses an isolated simulated portfolio. "
            "No IBKR quote request or order submission path is active."
        )
        print()
    elif not allow_order_submission:
        print(
            "SAFE MODE: Orion can connect to TWS and synchronize "
            "the Paper account, but IBKR order submission is disabled."
        )
        print()


def require_confirmation(
    execution_mode: str,
    cycles: int = 1,
    capital_profile: str = LivePaperTradingConfig.STANDARD_10000,
) -> bool:
    micro_shadow = (
        execution_mode == AutonomousPaperTradingConfig.SHADOW
        and capital_profile == LivePaperTradingConfig.MICRO_500
    )
    if cycles == 1:
        if micro_shadow:
            confirmation = MICRO_500_SHADOW_CONFIRMATION
        elif execution_mode == AutonomousPaperTradingConfig.SHADOW:
            confirmation = SHADOW_CONFIRMATION
        elif execution_mode == AutonomousPaperTradingConfig.EXIT_ONLY:
            confirmation = EXIT_ONLY_CONFIRMATION
        else:
            confirmation = BUY_AND_SELL_CONFIRMATION
    elif micro_shadow:
        confirmation = f"START {cycles} ORION MICRO 500 SHADOW CYCLES"
    elif execution_mode == AutonomousPaperTradingConfig.SHADOW:
        confirmation = f"START {cycles} ORION SHADOW CYCLES"
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
    shadow = "Shadow" in result.session.name
    print()
    print("=========================================")
    print(
        "ORION SHADOW RESULT"
        if shadow
        else "AUTONOMOUS IBKR PAPER RESULT"
    )
    print("=========================================")
    print(f"Completed cycles: {result.completed_cycles}")
    print(f"Failed cycles:    {result.failed_cycles}")
    print(f"Scanned symbols:  {result.total_scanned_symbols}")
    print(f"Analyzed symbols: {result.total_analyzed_symbols}")
    print(f"Skipped/failed:   {result.total_failed_symbols}")
    print(
        ("Shadow entries:   " if shadow else "Executed trades:  ")
        + str(result.total_executed_trades)
    )
    print(
        ("Shadow exits:     " if shadow else "Executed exits:   ")
        + str(result.total_executed_exits)
    )
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
    capital_profile = read_capital_profile()
    if (
        capital_profile == LivePaperTradingConfig.MICRO_500
        and execution_mode != AutonomousPaperTradingConfig.SHADOW
    ):
        raise RuntimeError(
            "MICRO_500 is currently restricted to SHADOW mode."
        )
    if (
        execution_mode == AutonomousPaperTradingConfig.SHADOW
        and allow_order_submission
    ):
        raise RuntimeError(
            "SHADOW mode requires ORION_IBKR_ALLOW_ORDERS=false."
        )
    cycles = read_cycle_count()
    scan_interval_seconds = read_scan_interval_seconds()
    exit_strategy = read_exit_strategy()
    pricing_plan = read_pricing_plan(
        default=(
            LivePaperTradingConfig.TIERED_PRICING
            if capital_profile == LivePaperTradingConfig.MICRO_500
            else LivePaperTradingConfig.FIXED_PRICING
        )
    )
    news_mode = read_news_mode()
    monthly_market_data_cost_eur = read_monthly_market_data_cost_eur(
        default=(
            3.0
            if capital_profile == LivePaperTradingConfig.MICRO_500
            else 0.0
        )
    )
    config = build_config(
        execution_mode=execution_mode,
        cycles=cycles,
        scan_interval_seconds=scan_interval_seconds,
        exit_strategy=exit_strategy,
        pricing_plan=pricing_plan,
        news_mode=news_mode,
        capital_profile=capital_profile,
        monthly_market_data_cost_eur=monthly_market_data_cost_eur,
    )

    print_runtime_mode(
        paper_account_id=paper_account_id,
        allow_order_submission=allow_order_submission,
        execution_mode=execution_mode,
        config=config,
    )

    if not require_confirmation(
        execution_mode,
        cycles,
        capital_profile,
    ):
        return

    shadow_mode = execution_mode == AutonomousPaperTradingConfig.SHADOW
    prefix = build_storage_prefix(
        execution_mode=execution_mode,
        capital_profile=capital_profile,
    )

    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id=paper_account_id,
        config=config,
        trade_journal_repository=JsonlTradeJournalRepository(
            path=f"{prefix}_trade_journal.jsonl",
        ),
        decision_journal_repository=JsonlTradeJournalRepository(
            path=f"{prefix}_decision_journal.jsonl",
        ),
        trading_session_repository=JsonTradingSessionRepository(
            path=f"{prefix}_trading_session.json",
        ),
        portfolio_repository=JsonPaperPortfolioRepository(
            path=f"{prefix}_paper_portfolio.json",
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
        news_event_repository=JsonlNewsEventRepository(
            path="data/ibkr_news_events.jsonl",
        ),
        news_assessment_repository=JsonlNewsAssessmentRepository(
            path="data/ibkr_news_assessments.jsonl",
        ),
        completed_trade_repository=JsonlCompletedTradeRepository(
            path=(
                f"{prefix}_completed_trades.jsonl"
                if shadow_mode
                else "data/ibkr_completed_trades.jsonl"
            ),
        ),
        allow_order_submission=allow_order_submission,
    )

    result = runtime.runner.run()

    print_result(result)


if __name__ == "__main__":
    main()
