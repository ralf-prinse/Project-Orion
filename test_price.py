from providers.yahoo_provider import YahooProvider


provider = YahooProvider()

symbol = "AAPL"
data = provider.get_market_data(symbol)

print("=== MARKET DATA ===")
print(f"Naam: {data.name}")
print(f"Symbool: {data.symbol}")
print(f"Beurs: {data.exchange}")
print(f"Valuta: {data.currency}")
print(f"Koers: {data.current_price}")
print(f"Open: {data.open_price}")
print(f"High: {data.high_price}")
print(f"Low: {data.low_price}")
print(f"Vorige close: {data.previous_close}")
print(f"Volume: {data.volume}")
print(f"Tijdstip: {data.timestamp}")