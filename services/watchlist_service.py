from pathlib import Path


class WatchlistService:
    """
    Laadt de aandelen die Orion automatisch moet scannen.
    """

    def __init__(self, watchlist_path: str = "config/watchlist.txt"):
        self.watchlist_path = Path(watchlist_path)

    def load_symbols(self) -> list[str]:
        if not self.watchlist_path.exists():
            raise FileNotFoundError(f"Watchlist niet gevonden: {self.watchlist_path}")

        symbols = []

        for line in self.watchlist_path.read_text(encoding="utf-8").splitlines():
            symbol = line.strip().upper()

            if symbol and not symbol.startswith("#"):
                symbols.append(symbol)

        return symbols