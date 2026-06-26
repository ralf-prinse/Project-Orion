import csv
import urllib.request
from pathlib import Path


class UniverseDownloader:
    """
    Downloadt Amerikaanse aandelenlijsten van NasdaqTrader.

    Bronnen:
    - nasdaqlisted.txt = Nasdaq-listed securities
    - otherlisted.txt = NYSE / AMEX / andere US exchanges

    Orion slaat alleen tickers lokaal op in:
    - data/universes/nasdaq.csv
    - data/universes/us_other.csv
    - data/universes/us_market.csv
    """

    NASDAQ_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
    OTHER_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/symdir/otherlisted.txt"

    def __init__(self, output_dir: str = "data/universes"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def update_us_market(self) -> dict:
        nasdaq_symbols = self._download_nasdaq_symbols()
        other_symbols = self._download_other_symbols()

        all_symbols = sorted(set(nasdaq_symbols + other_symbols))

        self._write_symbols("nasdaq.csv", nasdaq_symbols)
        self._write_symbols("us_other.csv", other_symbols)
        self._write_symbols("us_market.csv", all_symbols)

        return {
            "nasdaq": len(nasdaq_symbols),
            "us_other": len(other_symbols),
            "us_market": len(all_symbols),
        }

    def _download_nasdaq_symbols(self) -> list[str]:
        rows = self._download_pipe_file(self.NASDAQ_LISTED_URL)

        symbols = []

        for row in rows:
            symbol = row.get("Symbol", "").strip().upper()
            test_issue = row.get("Test Issue", "").strip().upper()
            etf = row.get("ETF", "").strip().upper()

            if not symbol:
                continue

            if symbol == "FILE CREATION TIME":
                continue

            if test_issue == "Y":
                continue

            if etf == "Y":
                continue

            if self._is_unwanted_symbol(symbol):
                continue

            symbols.append(self._normalize_yahoo_symbol(symbol))

        return sorted(set(symbols))

    def _download_other_symbols(self) -> list[str]:
        rows = self._download_pipe_file(self.OTHER_LISTED_URL)

        symbols = []

        for row in rows:
            symbol = row.get("ACT Symbol", "").strip().upper()
            test_issue = row.get("Test Issue", "").strip().upper()
            etf = row.get("ETF", "").strip().upper()

            if not symbol:
                continue

            if symbol == "FILE CREATION TIME":
                continue

            if test_issue == "Y":
                continue

            if etf == "Y":
                continue

            if self._is_unwanted_symbol(symbol):
                continue

            symbols.append(self._normalize_yahoo_symbol(symbol))

        return sorted(set(symbols))

    def _download_pipe_file(self, url: str) -> list[dict]:
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read().decode("utf-8", errors="ignore")

        lines = [
            line
            for line in content.splitlines()
            if line.strip() and not line.startswith("File Creation Time")
        ]

        reader = csv.DictReader(lines, delimiter="|")
        return list(reader)

    def _write_symbols(self, filename: str, symbols: list[str]) -> None:
        path = self.output_dir / filename

        with path.open("w", encoding="utf-8", newline="") as file:
            for symbol in symbols:
                file.write(f"{symbol}\n")

    def _normalize_yahoo_symbol(self, symbol: str) -> str:
        """
        Yahoo gebruikt vaak '-' voor share classes waar Nasdaq '.' gebruikt.
        Voorbeeld:
        BRK.B -> BRK-B
        """
        return symbol.replace(".", "-").strip().upper()

    def _is_unwanted_symbol(self, symbol: str) -> bool:
        """
        Eerste grove schoonmaak.

        We filteren:
        - warrants
        - rights
        - units
        - preferreds
        - tickers met rare suffixen
        """
        unwanted_suffixes = [
            "W",
            "WS",
            "WT",
            "U",
            "R",
            "P",
            "Q",
        ]

        if "^" in symbol:
            return True

        if "/" in symbol:
            return True

        if "$" in symbol:
            return True

        if len(symbol) > 6:
            return True

        for suffix in unwanted_suffixes:
            if symbol.endswith(suffix) and len(symbol) >= 5:
                return True

        return False