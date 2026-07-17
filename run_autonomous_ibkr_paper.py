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

CONFIRMATION = "START ONE AUTONOMOUS IBKR PAPER CYCLE"


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


def build_config() -> AutonomousPaperTradingConfig:
    live_config = LivePaperTradingConfig(
        watchlist_path="data/universes/ibkr_eu_us_validation.csv",
        initial_cash=10_000.0,
        max_symbols=6,
        max_open_positions=4,
        min_confidence=0.75,
        max_position_value=1000.0,
        max_position_size_pct=0.10,
    )

    return AutonomousPaperTradingConfig(
        live_config=live_config,
        cycles=1,
        sleep_seconds=0.0,
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
) -> None:
    print()
    print("=========================================")
    print("ORION AUTONOMOUS IBKR PAPER TRADING")
    print("=========================================")
    print(f"Account:           {mask_account_id(paper_account_id)}")
    print("TWS host:          127.0.0.1")
    print("TWS Paper port:    7497")
    print("Base currency:     EUR (required)")
    print("Cycles:            1")
    print("Maximum symbols:   6 (EU + US)")
    print("Maximum positions: 4")
    print(
        "Order submission: "
        + (
            "ENABLED"
            if allow_order_submission
            else "DISABLED"
        )
    )
    print("BUY execution:     IBKR")
    print("SELL execution:    IBKR")
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


def require_confirmation() -> bool:
    typed = input(
        f"Type exactly '{CONFIRMATION}' to continue: "
    ).strip()

    if typed != CONFIRMATION:
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
    print(f"Executed trades:  {result.total_executed_trades}")
    print(f"Rejected trades:  {result.total_rejected_trades}")
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

    print_runtime_mode(
        paper_account_id=paper_account_id,
        allow_order_submission=allow_order_submission,
    )

    if not require_confirmation():
        return

    runtime = IbkrAutonomousRuntimeFactory().build(
        paper_account_id=paper_account_id,
        config=build_config(),
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
