from providers.yahoo_provider import YahooProvider
from services.market_service import MarketService


provider = YahooProvider()
market_service = MarketService(provider)

symbol = "AAPL"
data = market_service.get_market_data(symbol)

print("=== MARKET SERVICE TEST ===")
print(f"Naam: {data.name}")
print(f"Symbool: {data.symbol}")
print(f"Koers: {data.current_price}")
print(f"Valuta: {data.currency}")
print(f"Volume: {data.volume}")