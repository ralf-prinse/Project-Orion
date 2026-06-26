from dataclasses import dataclass
from abc import ABC, abstractmethod

import pandas as pd


@dataclass
class HistoricalProviderStats:
    provider_name: str = ""
    requested_symbols: int = 0
    received_symbols: int = 0
    missing_symbols: int = 0
    cache_hits: int = 0
    fresh_downloads: int = 0
    duration_seconds: float = 0.0


class HistoricalDataProvider(ABC):
    """
    Abstracte basis voor historische marktdata.

    Iedere historische databron moet deze interface implementeren.
    De TechnicalScanner mag nooit rechtstreeks afhankelijk zijn van yfinance,
    Polygon, Alpaca of een andere databron.
    """

    def __init__(self):
        self.stats = HistoricalProviderStats(
            provider_name=self.__class__.__name__,
        )

    @abstractmethod
    def get_history(
        self,
        symbols: list[str],
        period: str = "6mo",
        interval: str = "1d",
    ) -> dict[str, pd.DataFrame]:
        pass
