from services.watchlist_service import WatchlistService


watchlist_service = WatchlistService()
symbols = watchlist_service.load_symbols()

print("=== WATCHLIST TEST ===")
print(f"Aantal aandelen: {len(symbols)}")

for symbol in symbols:
    print(symbol)