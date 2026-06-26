from engines.portfolio_engine import PortfolioEngine
from models.portfolio import Portfolio
from models.trade_plan import TradePlan


class TradePlanner:
    """
    TradePlanner 2.0

    Maakt van een ruwe actie een concreet handelsplan.

    De gebruiker ziet uiteindelijk alleen:
    - actie
    - aandeel
    - aantal

    Interne details zoals prijs en waarde blijven beschikbaar voor Orion,
    maar hoeven niet prominent in de GUI te staan.
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
        action = str(action).strip().upper()
        symbol = str(symbol).strip().upper()

        if action in ["BUY", "KOPEN"]:
            return self._create_buy_plan(
                symbol=symbol,
                price=price,
                portfolio=portfolio,
            )

        if action in ["SELL", "VERKOPEN"]:
            return self._create_sell_plan(
                symbol=symbol,
                price=price,
                portfolio=portfolio,
            )

        if action in ["HOLD", "VASTHOUDEN"]:
            return self._create_hold_plan(
                symbol=symbol,
                price=price,
                portfolio=portfolio,
            )

        return self._create_none_plan(
            symbol=symbol,
            price=price,
            portfolio=portfolio,
        )

    def _create_buy_plan(
        self,
        symbol: str,
        price: float,
        portfolio: Portfolio,
    ) -> TradePlan:
        quantity = self.portfolio_engine.calculate_buy_quantity(
            portfolio=portfolio,
            price=price,
        )

        estimated_value = self.portfolio_engine.calculate_position_value(
            quantity=quantity,
            price=price,
        )

        if quantity <= 0:
            return self._create_none_plan(
                symbol=symbol,
                price=price,
                portfolio=portfolio,
            )

        return TradePlan(
            action="BUY",
            symbol=symbol,
            quantity=quantity,
            estimated_price=price,
            estimated_value=estimated_value,
            currency=portfolio.currency,
        )

    def _create_sell_plan(
        self,
        symbol: str,
        price: float,
        portfolio: Portfolio,
    ) -> TradePlan:
        quantity = self._get_position_quantity(
            portfolio=portfolio,
            symbol=symbol,
        )

        estimated_value = self.portfolio_engine.calculate_position_value(
            quantity=quantity,
            price=price,
        )

        if quantity <= 0:
            return self._create_none_plan(
                symbol=symbol,
                price=price,
                portfolio=portfolio,
            )

        return TradePlan(
            action="SELL",
            symbol=symbol,
            quantity=quantity,
            estimated_price=price,
            estimated_value=estimated_value,
            currency=portfolio.currency,
        )

    def _create_hold_plan(
        self,
        symbol: str,
        price: float,
        portfolio: Portfolio,
    ) -> TradePlan:
        quantity = self._get_position_quantity(
            portfolio=portfolio,
            symbol=symbol,
        )

        estimated_value = self.portfolio_engine.calculate_position_value(
            quantity=quantity,
            price=price,
        )

        return TradePlan(
            action="HOLD",
            symbol=symbol,
            quantity=quantity,
            estimated_price=price,
            estimated_value=estimated_value,
            currency=portfolio.currency,
        )

    def _create_none_plan(
        self,
        symbol: str,
        price: float,
        portfolio: Portfolio,
    ) -> TradePlan:
        return TradePlan(
            action="NONE",
            symbol=symbol,
            quantity=0,
            estimated_price=price,
            estimated_value=0.0,
            currency=portfolio.currency,
        )

    def _get_position_quantity(
        self,
        portfolio: Portfolio,
        symbol: str,
    ) -> int:
        positions = getattr(portfolio, "positions", {})

        if not isinstance(positions, dict):
            return 0

        position = positions.get(symbol)

        if position is None:
            return 0

        if isinstance(position, dict):
            return int(position.get("quantity", 0))

        return int(getattr(position, "quantity", 0))