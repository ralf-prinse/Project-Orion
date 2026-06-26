from engines.decision_engine import DecisionEngine
from engines.technical_engine import TechnicalEngine
from engines.trade_planner import TradePlanner
from models.portfolio import Portfolio
from models.trade_plan import TradePlan
from providers.base_provider import BaseMarketProvider


class ScannerService:
    """
    Scant meerdere aandelen en maakt per aandeel een TradePlan.
    """

    def __init__(self, provider: BaseMarketProvider):
        self.provider = provider
        self.technical_engine = TechnicalEngine()
        self.decision_engine = DecisionEngine()
        self.trade_planner = TradePlanner()

    def scan(
        self,
        symbols: list[str],
        portfolio: Portfolio,
    ) -> list[TradePlan]:
        trade_plans = []

        for symbol in symbols:
            try:
                market_data = self.provider.get_market_data(symbol)
                history = self.provider.get_historical_data(
                    symbol,
                    period="6mo",
                    interval="1d",
                )

                analysis = self.technical_engine.analyze(history)

                action = self.decision_engine.decide(
                    technical_analysis=analysis,
                    has_position=False,
                )

                trade_plan = self.trade_planner.create_plan(
                    action=action,
                    symbol=symbol,
                    price=market_data.current_price,
                    portfolio=portfolio,
                )

                trade_plans.append(trade_plan)

            except Exception as error:
                print(f"Fout bij {symbol}: {error}")

        return trade_plans