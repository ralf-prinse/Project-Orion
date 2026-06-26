from pathlib import Path

from services.universe.base_universe_provider import BaseUniverseProvider


class LocalCsvUniverseProvider(BaseUniverseProvider):

    def __init__(self, csv_file: str):
        self.csv_file = Path(csv_file)

    def get_symbols(self) -> list[str]:

        if not self.csv_file.exists():
            return []

        symbols = []

        with self.csv_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            for line in file.readlines():

                symbol = line.strip().upper()

                if symbol:
                    symbols.append(symbol)

        return sorted(list(set(symbols)))