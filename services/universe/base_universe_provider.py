from abc import ABC, abstractmethod


class BaseUniverseProvider(ABC):
    """
    Basisklasse voor alle universe providers.

    Een provider levert uitsluitend tickers aan.

    Voorbeelden:

    - NASDAQ
    - NYSE
    - Euronext
    - Crypto
    """

    @abstractmethod
    def get_symbols(self) -> list[str]:
        raise NotImplementedError