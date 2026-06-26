from engines.portfolio_engine import PortfolioEngine
from models.portfolio import Portfolio


portfolio = Portfolio(
    cash=300.00,
    currency="EUR",
    max_position_percentage=0.35,
)

portfolio_engine = PortfolioEngine()

price = 275.15

quantity = portfolio_engine.calculate_buy_quantity(
    portfolio=portfolio,
    price=price,
)

position_value = portfolio_engine.calculate_position_value(
    quantity=quantity,
    price=price,
)

print("=== PORTFOLIO ENGINE TEST ===")
print(f"Cash: {portfolio.cash:.2f} {portfolio.currency}")
print(f"Max positie: {portfolio.max_position_value():.2f} {portfolio.currency}")
print(f"Aandeelprijs: {price:.2f}")
print(f"Aantal te kopen: {quantity}")
print(f"Totale aankoopwaarde: {position_value:.2f}")