from providers.base_provider import BaseMarketProvider
from models.market_data import MarketData


class MarketService:
    """
    Centrale toegangspoort voor marktdata.
    De rest van Orion praat met deze service, niet direct met providers.
    """

    def __init__(self, provider: BaseMarketProvider):
        self.provider = provider

    def get_market_data(self, symbol: str) -> MarketData:
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError("Symbol mag niet leeg zijn.")

        return self.provider.get_market_data(symbol)

    def get_current_price(self, symbol: str) -> float:
        market_data = self.get_market_data(symbol)
        return market_data.current_price