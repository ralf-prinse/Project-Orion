from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MarketQuote:
    symbol: str
    price: float
    volume: int
    previous_close: float | None = None
    change_percent: float | None = None


@dataclass
class MarketDataProviderStats:
    provider_name: str = ""
    requested_symbols: int = 0
    received_quotes: int = 0
    missing_quotes: int = 0
    duration_seconds: float = 0.0


class MarketDataProvider(ABC):
    """
    Abstracte basis voor alle market data providers.

    Iedere provider moet dezelfde interface ondersteunen.
    """

    def __init__(self):
        self.stats = MarketDataProviderStats()

    @abstractmethod
    def get_quotes(self, symbols: list[str]) -> list[MarketQuote]:
        """
        Haal actuele quote-data op voor een lijst symbolen.
        """
        raise NotImplementedError