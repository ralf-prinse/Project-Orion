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
from services.market.fx_rate_service import FxRateService
from services.portfolio_allocator import PortfolioAllocator
from services.stores.repositories.paper_portfolio_repository import (
    PaperPortfolioRepository,
)
from models.live_paper_trading_config import LivePaperTradingConfig
from services.ibkr.ibkr_portfolio_mapper import IbkrPortfolioMapper
from services.stores.repositories.trading_session_repository import (
    TradingSessionRepository,
)
from services.market_data.historical_cache import HistoricalCache
from services.market_data.yahoo_historical_provider import (
    YahooHistoricalDataProvider,
)
from services.ibkr.ibkr_news_provider import IbkrNewsProvider
from services.news.news_intelligence_service import NewsIntelligenceService
from services.ibkr.ibkr_quote_provider import IbkrQuoteProvider
from services.portfolio_concentration_gate import PortfolioConcentrationGate
from services.earnings_calendar_service import EarningsCalendarService


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
    historical_provider: YahooHistoricalDataProvider
    news_provider: object | None
    news_intelligence_service: NewsIntelligenceService | None


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
    NEWS_CLIENT_ID = 130
    QUOTE_CLIENT_ID = 140

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
        position_adoption_service=None,
        news_event_repository=None,
        news_assessment_repository=None,
        news_provider=None,
        completed_trade_repository=None,
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
        if runtime_config.live_config.base_currency.strip().upper() != "EUR":
            raise ValueError(
                "Autonomous IBKR Paper base currency must be EUR."
            )
        price_provider = YahooProvider()
        fx_rate_service = FxRateService()
        market_session_service = MarketSessionService()
        historical_provider = YahooHistoricalDataProvider(
            cache=HistoricalCache(ttl_minutes=15),
            batch_size=25,
        )
        resolved_news_provider = None
        news_intelligence_service = None
        if (
            runtime_config.live_config.news_mode
            == LivePaperTradingConfig.NEWS_SHADOW
        ):
            resolved_news_provider = (
                news_provider
                or IbkrNewsProvider(
                    host=host,
                    port=port,
                    client_id=self.NEWS_CLIENT_ID,
                )
            )
            news_intelligence_service = NewsIntelligenceService(
                provider=resolved_news_provider,
                event_repository=news_event_repository,
                assessment_repository=news_assessment_repository,
                lookback_hours=(
                    runtime_config.live_config.news_lookback_hours
                ),
                max_articles_per_symbol=(
                    runtime_config
                    .live_config
                    .news_max_articles_per_symbol
                ),
            )
        scanner = LivePaperMarketScanner(
            config=runtime_config.live_config,
            provider=price_provider,
            market_session_service=market_session_service,
            historical_provider=historical_provider,
        )
        allocator = PortfolioAllocator(
            fx_rate_service=fx_rate_service,
            require_live_fx=True,
            concentration_gate=PortfolioConcentrationGate(
                runtime_config.live_config.instrument_metadata_path
            ),
            earnings_calendar_service=EarningsCalendarService(
                runtime_config.live_config.earnings_calendar_path
            ),
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

        quote_provider = None
        if runtime_config.live_config.enable_execution_quality_gate:
            quote_provider = IbkrQuoteProvider(
                host=host,
                port=port,
                client_id=self.QUOTE_CLIENT_ID,
            )

        broker = IbkrBroker(
            transport=transport,
            enable_native_protective_orders=(
                runtime_config.live_config.enable_native_protective_orders
            ),
            quote_provider=quote_provider,
            max_bid_ask_spread_pct=(
                runtime_config.live_config.max_bid_ask_spread_pct
            ),
            max_quote_age_seconds=(
                runtime_config.live_config.max_quote_age_seconds
            ),
            max_entry_slippage_pct=(
                runtime_config.live_config.max_entry_slippage_pct
            ),
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
                mapper=IbkrPortfolioMapper(
                    base_currency="EUR",
                    fx_rate_service=fx_rate_service,
                    require_live_fx=True,
                ),
            )
        )

        runner = AutonomousPaperTradingRunner(
            config=runtime_config,
            scanner=scanner,
            allocator=allocator,
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
            position_adoption_service=position_adoption_service,
            news_intelligence_service=news_intelligence_service,
            completed_trade_repository=completed_trade_repository,
            protective_execution_reconciler=transport,
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
            historical_provider=historical_provider,
            news_provider=resolved_news_provider,
            news_intelligence_service=news_intelligence_service,
        )
