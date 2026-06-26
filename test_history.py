from providers.yahoo_provider import YahooProvider


provider = YahooProvider()

symbol = "AAPL"
history = provider.get_historical_data(symbol, period="1mo", interval="1d")

print("=== HISTORISCHE DATA TEST ===")
print(f"Symbool: {symbol}")
print(f"Aantal rijen: {len(history)}")
print()
print(history.tail())