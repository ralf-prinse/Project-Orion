from __future__ import annotations

from dataclasses import dataclass

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from providers.yahoo_provider import YahooProvider
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_account_service import IbkrAccountService
from services.ibkr.ibkr_broker import IbkrBroker
from services.ibkr.ibkr_order_transport import IbkrOrderTransport
from services.ibkr.ibkr_trading_session_sync_service import (
    IbkrTradingSessionSyncService,
)
from services.paper_trading_service import PaperTradingService
from services.position_exit_execution_service import (
    PositionExitExecutionService,
)
from services.stores.repositories.trade_journal_repository import (
    TradeJournalRepository,
)
from services.trading_cycle import TradingCycle
from services.live_paper_market_scanner import LivePaperMarketScanner
from services.market_session_service import MarketSessionService
from services.stores.repositories.paper_portfolio_repository import (
    PaperPortfolioRepository,
)
from services.stores.repositories.trading_session_repository import (
    TradingSessionRepository,
)


@dataclass(frozen=True)
class IbkrAutonomousRuntime:
    """
    Fully composed autonomous IBKR Paper Trading runtime.

    The exposed components make runtime wiring inspectable and testable.
    BUY and SELL execution intentionally share the same ExecutionEngine
    and therefore the same IbkrBroker instance.
    """

    runner: AutonomousPaperTradingRunner
    transport: IbkrOrderTransport
    broker: IbkrBroker
    execution_engine: ExecutionEngine
    paper_trading_service: PaperTradingService
    trading_cycle: TradingCycle
    position_exit_execution_service: PositionExitExecutionService
    account_service: IbkrAccountService
    trading_session_sync_service: IbkrTradingSessionSyncService
    price_provider: YahooProvider


class IbkrAutonomousRuntimeFactory:
    """
    Composition root for autonomous IBKR Paper Trading.

    This factory owns dependency construction only. It does not connect
    to TWS and does not start the autonomous runner.

    Order submission remains disabled by default and must be enabled
    explicitly for a controlled IBKR Paper Trading run.
    """

    DEFAULT_HOST = "127.0.0.1"
    PAPER_PORT = 7497
    ACCOUNT_CLIENT_ID = 110
    ORDER_CLIENT_ID = 120

    def build(
        self,
        *,
        paper_account_id: str,
        config: AutonomousPaperTradingConfig | None = None,
        trade_journal_repository: TradeJournalRepository | None = None,
        decision_journal_repository: (
            TradeJournalRepository | None
        ) = None,
        portfolio_repository: PaperPortfolioRepository | None = None,
        trading_session_repository: TradingSessionRepository | None = None,
        allow_order_submission: bool = False,
        host: str = DEFAULT_HOST,
        port: int = PAPER_PORT,
        account_client_id: int = ACCOUNT_CLIENT_ID,
        order_client_id: int = ORDER_CLIENT_ID,
    ) -> IbkrAutonomousRuntime:
        normalized_account_id = paper_account_id.strip().upper()

        if not normalized_account_id:
            raise ValueError(
                "paper_account_id must not be empty."
            )

        if not normalized_account_id.startswith("DU"):
            raise ValueError(
                "paper_account_id must reference an IBKR Paper "
                "account starting with 'DU'."
            )

        runtime_config = config or AutonomousPaperTradingConfig()
        price_provider = YahooProvider()
        market_session_service = MarketSessionService()
        scanner = LivePaperMarketScanner(
            config=runtime_config.live_config,
            provider=price_provider,
            market_session_service=market_session_service,
        )

        account_service = IbkrAccountService(
            host=host,
            port=port,
            client_id=account_client_id,
            expected_account_id=normalized_account_id,
        )

        transport = IbkrOrderTransport(
            paper_account_id=normalized_account_id,
            host=host,
            port=port,
            client_id=order_client_id,
            allow_order_submission=allow_order_submission,
        )

        broker = IbkrBroker(
            transport=transport,
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

        position_exit_execution_service = (
            PositionExitExecutionService(
                execution_engine=execution_engine,
            )
        )

        trading_session_sync_service = (
            IbkrTradingSessionSyncService(
                account_service=account_service,
                price_provider=price_provider,
            )
        )

        runner = AutonomousPaperTradingRunner(
            config=runtime_config,
            scanner=scanner,
            trading_cycle=trading_cycle,
            portfolio_repository=portfolio_repository,
            trading_session_repository=trading_session_repository,
            trade_journal_repository=trade_journal_repository,
            decision_journal_repository=(
                decision_journal_repository
            ),
            price_provider=price_provider,
            position_exit_execution_service=(
                position_exit_execution_service
            ),
            trading_session_sync_service=(
                trading_session_sync_service
            ),
            market_session_service=market_session_service,
        )

        return IbkrAutonomousRuntime(
            runner=runner,
            transport=transport,
            broker=broker,
            execution_engine=execution_engine,
            paper_trading_service=paper_trading_service,
            trading_cycle=trading_cycle,
            position_exit_execution_service=(
                position_exit_execution_service
            ),
            account_service=account_service,
            trading_session_sync_service=(
                trading_session_sync_service
            ),
            price_provider=price_provider,
        )
