from engines.technical_engine import TechnicalEngine
from providers.yahoo_provider import YahooProvider


provider = YahooProvider()
technical_engine = TechnicalEngine()

symbol = "AAPL"

history = provider.get_historical_data(symbol, period="3mo", interval="1d")
rsi = technical_engine.calculate_rsi(history)

print("=== RSI TEST ===")
print(f"Symbool: {symbol}")
print(f"Aantal rijen: {len(history)}")
print(f"RSI: {rsi:.2f}")