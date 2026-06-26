from concurrent.futures import ThreadPoolExecutor, as_completed

from engines.decision_engine import DecisionEngine
from engines.technical_engine import TechnicalEngine
from engines.trade_planner import TradePlanner
from models.portfolio import Portfolio
from models.trade_plan import TradePlan
from providers.base_provider import BaseMarketProvider
from services.market_filter import MarketFilter
from services.universe_manager import UniverseManager


class ScannerService:

    def __init__(
        self,
        provider: BaseMarketProvider,
        universe_manager: UniverseManager,
        max_workers: int = 8,
    ):
        self.provider = provider
        self.universe_manager = universe_manager

        self.technical_engine = TechnicalEngine()
        self.decision_engine = DecisionEngine()
        self.trade_planner = TradePlanner()

        self.market_filter = MarketFilter()

        self.max_workers = max_workers

    def scan(
        self,
        symbols: list[str] | None,
        portfolio: Portfolio,
        universe_name: str = "swing",
    ) -> list[TradePlan]:

        if symbols is None:
            symbols = self.universe_manager.get_symbols(
                universe_name
            )

        plans = []

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = {
                executor.submit(
                    self.scan_symbol,
                    symbol,
                    portfolio,
                ): symbol
                for symbol in symbols
            }

            for future in as_completed(futures):

                plan = future.result()

                if plan is not None:
                    plans.append(plan)

        plans.sort(
            key=lambda p: (
                p.action != "BUY",
                p.symbol,
            )
        )

        return plans

    def scan_symbol(
        self,
        symbol: str,
        portfolio: Portfolio,
    ):

        try:

            market_data = self.provider.get_market_data(symbol)

            filter_result = self.market_filter.accept(
                symbol=symbol,
                price=market_data.current_price,
            )

            if not filter_result.accepted:
                return None

            history = self.provider.get_historical_data(
                symbol,
                period="6mo",
                interval="1d",
            )

            analysis = self.technical_engine.analyze(history)

            action = self.decision_engine.decide(
                technical_analysis=analysis,
                has_position=portfolio.has_position(symbol),
            )

            return self.trade_planner.create_plan(
                action=action,
                symbol=symbol,
                price=market_data.current_price,
                portfolio=portfolio,
            )

        except Exception:
            return None