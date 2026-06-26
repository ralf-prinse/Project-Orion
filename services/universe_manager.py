from dataclasses import dataclass

from services.universe.local_csv_provider import LocalCsvUniverseProvider


@dataclass
class Universe:
    name: str
    description: str
    providers: list


class UniverseManager:
    """
    UniverseManager 2.0

    Combineert meerdere providers tot één universe.

    Later kunnen we toevoegen:

    - NASDAQ
    - NYSE
    - AMEX
    - EURONEXT
    - CRYPTO
    """

    def __init__(self):

        self.universes = {
            "swing": Universe(
                name="Swing",
                description="Swing Trading Universe",
                providers=[
                    LocalCsvUniverseProvider(
                        "data/universes/swing.csv"
                    ),
                ],
            ),
        }

    def get_universe(self, name: str) -> Universe:

        return self.universes[name]

    def get_symbols(self, name: str) -> list[str]:

        universe = self.get_universe(name)

        symbols = []

        for provider in universe.providers:

            symbols.extend(
                provider.get_symbols()
            )

        return sorted(
            list(
                set(symbols)
            )
        )

    def available_universes(self):

        return list(
            self.universes.keys()
        )