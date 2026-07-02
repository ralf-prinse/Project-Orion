from models.portfolio import Portfolio
from providers.yahoo_provider import YahooProvider
from services.scanner_service import ScannerService
from services.watchlist_service import WatchlistService
from unittest.mock import Mock


watchlist_service = WatchlistService()
symbols = watchlist_service.load_symbols()

provider = YahooProvider()
universe_manager = Mock()
scanner_service = ScannerService(provider, universe_manager)

portfolio = Portfolio(
    cash=300.00,
    currency="EUR",
    max_position_percentage=0.35,
)

trade_plans = scanner_service.scan(
    symbols=symbols,
    portfolio=portfolio,
)

print("=== SCANNER SERVICE TEST ===")

for plan in trade_plans:
    print(
        f"{plan.symbol} | "
        f"Actie: {plan.action} | "
        f"Aantal: {plan.quantity} | "
        f"Waarde: {plan.estimated_value:.2f} {plan.currency}"
    )