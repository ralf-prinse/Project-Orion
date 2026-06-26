from dataclasses import dataclass


@dataclass(frozen=True)
class MarketUniverse:
    name: str
    symbols: list[str]


class UniverseManager:
    """
    Beheert welke aandelen Orion mag scannen.

    Let op:
    Dit is nog geen volledige wereldwijde marktfeed.
    Dit is de eerste echte universe-laag, zodat de scanner niet meer
    afhankelijk is van alleen een losse watchlist.
    """

    def __init__(self):
        self.universes = {
            "core": self._core_universe(),
            "swing": self._swing_universe(),
            "aex": self._aex_universe(),
            "nasdaq_100_sample": self._nasdaq_100_sample(),
            "sp500_sample": self._sp500_sample(),
        }

    def get_universe(self, name: str = "swing") -> MarketUniverse:
        name = name.strip().lower()

        if name not in self.universes:
            available = ", ".join(self.universes.keys())
            raise ValueError(
                f"Onbekende universe: {name}. Beschikbaar: {available}"
            )

        return self.universes[name]

    def get_symbols(self, name: str = "swing") -> list[str]:
        return self.get_universe(name).symbols

    def list_universes(self) -> list[str]:
        return list(self.universes.keys())

    def _core_universe(self) -> MarketUniverse:
        return MarketUniverse(
            name="core",
            symbols=[
                "AAPL",
                "MSFT",
                "NVDA",
                "TSLA",
                "AMZN",
                "META",
                "GOOGL",
                "AMD",
                "ASML.AS",
                "ADYEN.AS",
            ],
        )

    def _swing_universe(self) -> MarketUniverse:
        """
        Eerste serieuze swing-trading universe.

        Focus:
        - liquide aandelen
        - bekende namen
        - genoeg volume
        - geschikt voor trades van uren tot dagen
        """
        return MarketUniverse(
            name="swing",
            symbols=[
                # Mega cap tech
                "AAPL",
                "MSFT",
                "NVDA",
                "META",
                "AMZN",
                "GOOGL",
                "TSLA",
                "AMD",
                "AVGO",
                "NFLX",

                # Semiconductors
                "SMCI",
                "MU",
                "INTC",
                "QCOM",
                "ARM",
                "TSM",
                "ASML.AS",

                # Fintech / growth
                "COIN",
                "SQ",
                "PYPL",
                "SHOP",
                "PLTR",
                "SNOW",
                "CRM",

                # High volume / momentum
                "MARA",
                "RIOT",
                "SOFI",
                "RIVN",
                "LCID",
                "UBER",
                "ABNB",

                # Defensive / liquid
                "JPM",
                "BAC",
                "XOM",
                "CVX",
                "LLY",
                "UNH",
                "NKE",

                # Dutch / European focus
                "ASML.AS",
                "ADYEN.AS",
                "INGA.AS",
                "ABN.AS",
                "PHIA.AS",
                "ASM.AS",
                "BESI.AS",
                "REL.AS",
                "WKL.AS",
            ],
        )

    def _aex_universe(self) -> MarketUniverse:
        return MarketUniverse(
            name="aex",
            symbols=[
                "ASML.AS",
                "ADYEN.AS",
                "INGA.AS",
                "ABN.AS",
                "PHIA.AS",
                "ASM.AS",
                "BESI.AS",
                "REL.AS",
                "WKL.AS",
                "KPN.AS",
                "HEIA.AS",
                "AKZA.AS",
                "MT.AS",
                "NN.AS",
                "PRX.AS",
                "RAND.AS",
                "REN.AS",
                "SHELL.AS",
                "UMG.AS",
                "UNA.AS",
            ],
        )

    def _nasdaq_100_sample(self) -> MarketUniverse:
        return MarketUniverse(
            name="nasdaq_100_sample",
            symbols=[
                "AAPL",
                "MSFT",
                "NVDA",
                "AMZN",
                "META",
                "GOOGL",
                "GOOG",
                "AVGO",
                "TSLA",
                "COST",
                "NFLX",
                "AMD",
                "PEP",
                "ADBE",
                "CSCO",
                "TMUS",
                "INTC",
                "QCOM",
                "AMAT",
                "INTU",
                "TXN",
                "AMGN",
                "ISRG",
                "BKNG",
                "LRCX",
                "MU",
                "PANW",
                "ADI",
                "KLAC",
                "SNPS",
            ],
        )

    def _sp500_sample(self) -> MarketUniverse:
        return MarketUniverse(
            name="sp500_sample",
            symbols=[
                "AAPL",
                "MSFT",
                "NVDA",
                "AMZN",
                "META",
                "GOOGL",
                "BRK-B",
                "LLY",
                "AVGO",
                "JPM",
                "TSLA",
                "XOM",
                "UNH",
                "V",
                "MA",
                "PG",
                "JNJ",
                "HD",
                "COST",
                "ABBV",
                "BAC",
                "NFLX",
                "KO",
                "MRK",
                "CVX",
                "WMT",
                "AMD",
                "CRM",
                "ADBE",
                "PEP",
            ],
        )