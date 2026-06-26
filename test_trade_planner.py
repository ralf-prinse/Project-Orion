from engines.decision_engine import DecisionEngine
from engines.technical_engine import TechnicalEngine
from engines.trade_planner import TradePlanner
from models.portfolio import Portfolio
from providers.yahoo_provider import YahooProvider


provider = YahooProvider()
technical_engine = TechnicalEngine()
decision_engine = DecisionEngine()
trade_planner = TradePlanner()

portfolio = Portfolio(
    cash=300.00,
    currency="EUR",
    max_position_percentage=0.35,
)

symbol = "NOK"

market_data = provider.get_market_data(symbol)
history = provider.get_historical_data(symbol, period="6mo", interval="1d")

analysis = technical_engine.analyze(history)
action = "BUY"

trade_plan = trade_planner.create_plan(
    action=action,
    symbol=symbol,
    price=market_data.current_price,
    portfolio=portfolio,
)

print("=== TRADE PLANNER TEST ===")
print(f"Symbool: {trade_plan.symbol}")
print(f"Actie: {trade_plan.action}")
print(f"Aantal: {trade_plan.quantity}")
print(f"Geschatte prijs: {trade_plan.estimated_price:.2f}")
print(f"Geschatte waarde: {trade_plan.estimated_value:.2f} {trade_plan.currency}")