from abc import ABC, abstractmethod

import pandas as pd

from models.market_data import MarketData


class BaseMarketProvider(ABC):
    """
    Basisklasse voor alle marktdata-providers.
    """

    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        """
        Haalt de actuele prijs op van een aandeel.
        """
        pass

    @abstractmethod
    def get_market_data(self, symbol: str) -> MarketData:
        """
        Haalt actuele marktdata op van een aandeel.
        """
        pass

    @abstractmethod
    def get_historical_data(
        self,
        symbol: str,
        period: str = "3mo",
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Haalt historische koersdata op.
        """
        pass