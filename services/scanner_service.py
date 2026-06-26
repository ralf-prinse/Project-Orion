from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Optional

from engines.decision_engine import DecisionEngine
from engines.technical_engine import TechnicalEngine
from engines.trade_planner import TradePlanner
from models.portfolio import Portfolio
from models.trade_plan import TradePlan
from providers.base_provider import BaseMarketProvider
from services.universe_manager import UniverseManager


@dataclass
class ScanResult:
    symbol: str
    success: bool
    trade_plan: Optional[TradePlan] = None
    error: Optional[str] = None


class ScannerService:
    """
    ScannerService 2.0

    Verantwoordelijkheid:
    - bepaalt welke symbols gescand worden via UniverseManager;
    - haalt marktdata op via provider;
    - voert technische analyse uit;
    - laat DecisionEngine de eindactie bepalen;
    - laat TradePlanner het concrete TradePlan maken.

    De GUI ziet alleen TradePlans.
    Indicatoren en analyse blijven intern.
    """

    def __init__(
        self,
        provider: BaseMarketProvider,
        universe_manager: UniverseManager | None = None,
        max_workers: int = 8,
    ):
        self.provider = provider
        self.universe_manager = universe_manager or UniverseManager()
        self.technical_engine = TechnicalEngine()
        self.decision_engine = DecisionEngine()
        self.trade_planner = TradePlanner()
        self.max_workers = max_workers

    def scan(
        self,
        symbols: list[str] | None = None,
        portfolio: Portfolio | None = None,
        universe_name: str = "swing",
    ) -> list[TradePlan]:
        if portfolio is None:
            portfolio = Portfolio(cash=0, positions={})

        if symbols is None:
            symbols = self.universe_manager.get_symbols(universe_name)

        results = self._scan_parallel(symbols=symbols, portfolio=portfolio)

        trade_plans = [
            result.trade_plan
            for result in results
            if result.success and result.trade_plan is not None
        ]

        return self._sort_trade_plans(trade_plans)

    def _scan_parallel(
        self,
        symbols: list[str],
        portfolio: Portfolio,
    ) -> list[ScanResult]:
        results: list[ScanResult] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {
                executor.submit(self._scan_symbol, symbol, portfolio): symbol
                for symbol in symbols
            }

            for future in as_completed(future_map):
                symbol = future_map[future]

                try:
                    results.append(future.result())
                except Exception as error:
                    results.append(
                        ScanResult(
                            symbol=symbol,
                            success=False,
                            error=str(error),
                        )
                    )

        return results

    def _scan_symbol(
        self,
        symbol: str,
        portfolio: Portfolio,
    ) -> ScanResult:
        try:
            market_data = self.provider.get_market_data(symbol)

            history = self.provider.get_historical_data(
                symbol,
                period="6mo",
                interval="1d",
            )

            analysis = self.technical_engine.analyze(history)

            has_position = self._portfolio_has_position(portfolio, symbol)

            action = self.decision_engine.decide(
                technical_analysis=analysis,
                has_position=has_position,
            )

            trade_plan = self.trade_planner.create_plan(
                action=action,
                symbol=symbol,
                price=market_data.current_price,
                portfolio=portfolio,
            )

            return ScanResult(
                symbol=symbol,
                success=True,
                trade_plan=trade_plan,
            )

        except Exception as error:
            return ScanResult(
                symbol=symbol,
                success=False,
                error=str(error),
            )

    def _portfolio_has_position(self, portfolio: Portfolio, symbol: str) -> bool:
        positions = getattr(portfolio, "positions", {})

        if isinstance(positions, dict):
            position = positions.get(symbol)
            if position is None:
                return False

            quantity = getattr(position, "quantity", 0)
            if isinstance(position, dict):
                quantity = position.get("quantity", 0)

            return quantity > 0

        return False

    def _sort_trade_plans(self, trade_plans: list[TradePlan]) -> list[TradePlan]:
        priority = {
            "KOPEN": 0,
            "BUY": 0,
            "VERKOPEN": 1,
            "SELL": 1,
            "VASTHOUDEN": 2,
            "HOLD": 2,
            "GEEN ACTIE": 3,
            "NO_ACTION": 3,
        }

        return sorted(
            trade_plans,
            key=lambda plan: priority.get(str(plan.action).upper(), 99),
        )
        