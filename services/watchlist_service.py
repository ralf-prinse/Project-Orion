from pathlib import Path


class WatchlistService:
    """
    Laadt de aandelen die Orion automatisch moet scannen.

    Source of truth:
    data/universes/swing.csv
    """

    def __init__(self, watchlist_path: str = "data/universes/swing.csv"):
        self.watchlist_path = Path(watchlist_path)

    def load_symbols(self) -> list[str]:
        if not self.watchlist_path.exists():
            raise FileNotFoundError(f"Universe niet gevonden: {self.watchlist_path}")

        symbols = []

        for line in self.watchlist_path.read_text(encoding="utf-8").splitlines():
            symbol = line.strip().upper()

            if symbol and not symbol.startswith("#"):
                symbols.append(symbol)

        return sorted(list(set(symbols)))