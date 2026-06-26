from pathlib import Path


class UniverseLoader:
    """
    Centrale loader voor aandelen-universums.

    Verantwoordelijkheid:
    - Symbolen laden uit data/universes/
    - Duplicaten verwijderen
    - Lege regels overslaan
    - Symbolen normaliseren naar uppercase

    Bewust géén scanner-logica.
    """

    DEFAULT_UNIVERSE_FILE = Path("data/universes/us_market.csv")

    def __init__(self, universe_file: Path | str | None = None):
        self.universe_file = Path(universe_file) if universe_file else self.DEFAULT_UNIVERSE_FILE

    def load_symbols(self, limit: int | None = None) -> list[str]:
        if not self.universe_file.exists():
            raise FileNotFoundError(f"Universebestand niet gevonden: {self.universe_file}")

        symbols: list[str] = []
        seen: set[str] = set()

        with self.universe_file.open("r", encoding="utf-8") as file:
            for line in file:
                symbol = line.strip().upper()

                if not symbol:
                    continue

                if symbol in seen:
                    continue

                seen.add(symbol)
                symbols.append(symbol)

                if limit is not None and len(symbols) >= limit:
                    break

        return symbols