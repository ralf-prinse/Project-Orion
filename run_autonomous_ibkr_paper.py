from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from models.autonomous_paper_trading_config import AutonomousPaperTradingConfig
from models.live_paper_trading_config import LivePaperTradingConfig
from models.trading_session import TradingSession
from providers.yahoo_provider import YahooProvider
from services.autonomous_paper_trading_runner import AutonomousPaperTradingRunner
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_broker import IbkrBroker
from services.ibkr.ibkr_order_transport import IbkrOrderTransport
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper
from services.paper_trading_service import PaperTradingService
from services.stores.jsonl_trade_journal_repository import JsonlTradeJournalRepository
from services.trading_cycle import TradingCycle


CONFIRMATION = "START ONE AUTONOMOUS IBKR PAPER CYCLE"


class InMemoryTradingSessionRepository:
    def __init__(self, session: TradingSession) -> None:
        self._session = session

    def exists(self) -> bool:
        return True

    def load(self) -> TradingSession:
        return self._session

    def save(self, session: TradingSession) -> None:
        self._session = session


@dataclass(frozen=True)
class DisabledExitResult:
    executed: bool = False


class BuyOnlyExitEngine:
    """Prevents local-only SELL handling during the first IBKR validation."""

    def execute(self, *, portfolio, decision) -> DisabledExitResult:
        return DisabledExitResult()


def require_account_id() -> str:
    account_id = os.environ.get("ORION_IBKR_PAPER_ACCOUNT_ID", "").strip().upper()
    if not account_id.startswith("DU"):
        raise RuntimeError(
            "Set ORION_IBKR_PAPER_ACCOUNT_ID to the DU-prefixed TWS Paper account."
        )
    return account_id


def read_ibkr_session(account_id: str) -> TradingSession:
    account_service = IbkrAccountService(
        host="127.0.0.1",
        port=7497,
        client_id=110,
        timeout_seconds=15.0,
    )
    price_provider = YahooProvider()

    account_service.connect()
    try:
        account = account_service.read_account()

        if account.account_id.strip().upper() != account_id:
            raise RuntimeError(
                "Connected TWS Paper account does not match "
                "ORION_IBKR_PAPER_ACCOUNT_ID."
            )

        positions = account_service.read_positions()
    finally:
        account_service.disconnect()

    current_prices = {
        position.symbol.strip().upper(): price_provider.get_current_price(
            position.symbol.strip().upper()
        )
        for position in positions
    }

    portfolio = IbkrPortfolioMapper().map(
        account=account,
        positions=positions,
        current_prices=current_prices,
    )
    return TradingSession(
        name="Orion Autonomous IBKR Paper Validation",
        portfolio=portfolio,
    )


def main() -> None:
    account_id = require_account_id()
    session = read_ibkr_session(account_id)

    transport = IbkrOrderTransport(
        paper_account_id=account_id,
        host="127.0.0.1",
        port=7497,
        client_id=141,
        allow_order_submission=True,
        disconnect_after_order=True,
    )
    broker = IbkrBroker(
        transport=transport,
        timeout_seconds=45.0,
        exchange="SMART",
        currency="USD",
    )
    execution_engine = ExecutionEngine(broker=broker)
    trading_service = PaperTradingService(execution_engine=execution_engine)
    trading_cycle = TradingCycle(paper_trading_service=trading_service)

    live_config = LivePaperTradingConfig(
        watchlist_path="data/universes/ibkr_us_validation.csv",
        initial_cash=session.cash,
        max_symbols=1,
        max_open_positions=max(session.open_positions + 1, 1),
        min_confidence=0.75,
        max_position_value=150.0,
    )
    config = AutonomousPaperTradingConfig(
        live_config=live_config,
        cycles=1,
        sleep_seconds=0.0,
        stop_on_exception=True,
        print_cycle_summary=True,
    )

    print("\n=========================================")
    print("ORION AUTONOMOUS IBKR PAPER VALIDATION")
    print("=========================================")
    print(f"Account:          {account_id[:2]}*****{account_id[-2:]}")
    print(f"Starting cash:    {session.cash:.2f}")
    print(f"Open positions:   {session.open_positions}")
    print("Cycles:           1")
    print("Exit execution:   DISABLED (BUY-only validation)")
    print("Automatic retry:  NO")
    print("=========================================\n")

    typed = input(f"Type exactly '{CONFIRMATION}' to continue: ").strip()
    if typed != CONFIRMATION:
        print("Confirmation mismatch. No runner was started.")
        return

    runner = AutonomousPaperTradingRunner(
        config=config,
        trading_cycle=trading_cycle,
        trading_session_repository=InMemoryTradingSessionRepository(session),
        trade_journal_repository=JsonlTradeJournalRepository(
            path="data/ibkr_autonomous_trade_journal.jsonl",
        ),
        exit_engine=BuyOnlyExitEngine(),
    )
    result = runner.run()

    print("\n=========================================")
    print("AUTONOMOUS IBKR PAPER RESULT")
    print("=========================================")
    print(f"Completed cycles: {result.completed_cycles}")
    print(f"Failed cycles:    {result.failed_cycles}")
    print(f"Executed trades:  {result.total_executed_trades}")
    print(f"Rejected trades:  {result.total_rejected_trades}")
    print(f"Final cash:       {result.final_cash:.2f}")
    print(f"Final equity:     {result.final_equity:.2f}")
    print(f"Open positions:   {result.session.open_positions}")
    print("=========================================\n")


if __name__ == "__main__":
    main()
