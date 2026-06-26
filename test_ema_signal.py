from engines.technical_engine import TechnicalEngine
from providers.yahoo_provider import YahooProvider


provider = YahooProvider()
technical_engine = TechnicalEngine()

symbol = "AAPL"

history = provider.get_historical_data(symbol, period="6mo", interval="1d")

ema_20 = technical_engine.calculate_ema(history, 20)
ema_50 = technical_engine.calculate_ema(history, 50)
trend = technical_engine.interpret_ema_trend(history)

print("=== EMA SIGNAL TEST ===")
print(f"Symbool: {symbol}")
print(f"EMA 20: {ema_20:.2f}")
print(f"EMA 50: {ema_50:.2f}")
print(f"Intern trendsignaal: {trend}")