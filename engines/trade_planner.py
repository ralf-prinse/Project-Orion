from engines.portfolio_engine import PortfolioEngine
from models.portfolio import Portfolio
from models.trade_plan import TradePlan


class TradePlanner:
    """
    Maakt een praktisch handelsplan op basis van een actie, portfolio en koers.
    """

    def __init__(self):
        self.portfolio_engine = PortfolioEngine()

    def create_plan(
        self,
        action: str,
        symbol: str,
        price: float,
        portfolio: Portfolio,
    ) -> TradePlan:
        action = action.strip().upper()
        symbol = symbol.strip().upper()

        if action != "BUY":
            return TradePlan(
                action=action,
                symbol=symbol,
                quantity=0,
                estimated_price=price,
                estimated_value=0.0,
                currency=portfolio.currency,
            )

        quantity = self.portfolio_engine.calculate_buy_quantity(
            portfolio=portfolio,
            price=price,
        )

        estimated_value = self.portfolio_engine.calculate_position_value(
            quantity=quantity,
            price=price,
        )

        if quantity <= 0:
            return TradePlan(
                action="NONE",
                symbol=symbol,
                quantity=0,
                estimated_price=price,
                estimated_value=0.0,
                currency=portfolio.currency,
            )

        return TradePlan(
            action="BUY",
            symbol=symbol,
            quantity=quantity,
            estimated_price=price,
            estimated_value=estimated_value,
            currency=portfolio.currency,
        )