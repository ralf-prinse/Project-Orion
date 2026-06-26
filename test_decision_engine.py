from engines.decision_engine import DecisionEngine
from engines.technical_engine import TechnicalEngine
from providers.yahoo_provider import YahooProvider


provider = YahooProvider()
technical_engine = TechnicalEngine()
decision_engine = DecisionEngine()

symbol = "AAPL"

history = provider.get_historical_data(symbol, period="3mo", interval="1d")
rsi = technical_engine.calculate_rsi(history)
rsi_signal = technical_engine.interpret_rsi(rsi)
action = decision_engine.decide_from_rsi_signal(rsi_signal)

print("=== DECISION ENGINE TEST ===")
print(f"Symbool: {symbol}")
print(f"Intern RSI-signaal: {rsi_signal}")
print(f"Gebruikersactie: {action}")