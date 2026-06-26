from engines.decision_engine import DecisionEngine
from engines.technical_engine import TechnicalEngine
from providers.yahoo_provider import YahooProvider


provider = YahooProvider()
technical_engine = TechnicalEngine()
decision_engine = DecisionEngine()

symbol = "AAPL"

history = provider.get_historical_data(symbol, period="6mo", interval="1d")
analysis = technical_engine.analyze(history)

action_without_position = decision_engine.decide(
    technical_analysis=analysis,
    has_position=False,
)

action_with_position = decision_engine.decide(
    technical_analysis=analysis,
    has_position=True,
)

print("=== FULL ANALYSIS TEST ===")
print(f"Symbool: {symbol}")
print(f"Actie zonder positie: {action_without_position}")
print(f"Actie met positie: {action_with_position}")