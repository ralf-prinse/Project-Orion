from models.portfolio import Portfolio
from services.portfolio.models import PortfolioPosition, PortfolioState


class PortfolioStateAdapter:
    """
    Converts the runtime Portfolio model into a deterministic PortfolioState.

    This adapter keeps compatibility code out of MainWindow and presenters.
    It performs no analytics, validation or presentation formatting.
    """

    def from_portfolio(self, portfolio: Portfolio) -> PortfolioState:
        positions: dict[str, PortfolioPosition] = {}

        for symbol, position in portfolio.positions.items():
            if isinstance(position, dict):
                quantity = int(position.get("quantity", 0))
                average_price = float(position.get("average_price", 0.0))
                currency = position.get("currency", portfolio.currency)
            else:
                quantity = int(position.quantity)
                average_price = float(position.average_price)
                currency = position.currency

            positions[symbol.upper()] = PortfolioPosition(
                symbol=symbol.upper(),
                quantity=quantity,
                average_price=average_price,
                current_price=average_price,
            )

        return PortfolioState(
            cash=float(portfolio.cash),
            positions=positions,
            currency=portfolio.currency,
        )