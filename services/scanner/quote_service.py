from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
import json

from services.market_data.base_provider import MarketDataProvider, MarketQuote
from services.market_data.yahoo_provider import YahooMarketDataProvider


@dataclass
class Quote:
    symbol: str
    price: float
    volume: int
    previous_close: float | None = None
    change_percent: float | None = None


@dataclass
class QuoteServiceStats:
    requested_symbols: int = 0
    cached_quotes: int = 0
    fresh_quotes: int = 0
    missing_quotes: int = 0
    negative_cache_hits: int = 0


class QuoteService:
    """
    Orchestrator voor quote-data.

    Belangrijk:
    - QuoteService gebruikt een MarketDataProvider.
    - QuoteService gebruikt zelf geen yfinance.
    - Caching blijft hier centraal geregeld.
    - Niet-gevonden symbolen worden tijdelijk negatief gecachet.
    """

    def __init__(
        self,
        provider: MarketDataProvider | None = None,
        cache_file: Path | str = "data/cache/quotes.json",
        cache_ttl_minutes: int = 15,
        negative_cache_ttl_minutes: int = 15,
        use_cache: bool = True,
    ):
        self.provider = provider or YahooMarketDataProvider(batch_size=500)
        self.cache_file = Path(cache_file)
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self.negative_cache_ttl = timedelta(minutes=negative_cache_ttl_minutes)
        self.use_cache = use_cache
        self.stats = QuoteServiceStats()

    def get_quotes(self, symbols: list[str]) -> list[Quote]:
        clean_symbols = self._clean_symbols(symbols)

        self.stats = QuoteServiceStats(
            requested_symbols=len(clean_symbols),
        )

        if not clean_symbols:
            return []

        cache = self._load_cache() if self.use_cache else {}

        cached_quotes: list[Quote] = []
        missing_symbols: list[str] = []
        negative_cache_hits = 0

        now = datetime.now()

        for symbol in clean_symbols:
            cached_quote = self._get_cached_quote(
                cache=cache,
                symbol=symbol,
                now=now,
            )

            if cached_quote is not None:
                cached_quotes.append(cached_quote)
                continue

            if self._is_negative_cached(
                cache=cache,
                symbol=symbol,
                now=now,
            ):
                negative_cache_hits += 1
                continue

            missing_symbols.append(symbol)

        fresh_market_quotes = self.provider.get_quotes(missing_symbols)
        fresh_quotes = [
            self._from_market_quote(market_quote)
            for market_quote in fresh_market_quotes
        ]

        fresh_symbols = {
            quote.symbol
            for quote in fresh_quotes
        }

        provider_missing_symbols = [
            symbol
            for symbol in missing_symbols
            if symbol not in fresh_symbols
        ]

        if self.use_cache:
            if fresh_quotes:
                self._update_cache(
                    cache=cache,
                    quotes=fresh_quotes,
                    timestamp=now,
                )

            if provider_missing_symbols:
                self._update_negative_cache(
                    cache=cache,
                    symbols=provider_missing_symbols,
                    timestamp=now,
                )

        quote_map = {
            quote.symbol: quote
            for quote in cached_quotes + fresh_quotes
        }

        final_quotes = [
            quote_map[symbol]
            for symbol in clean_symbols
            if symbol in quote_map
        ]

        self.stats.cached_quotes = len(cached_quotes)
        self.stats.fresh_quotes = len(fresh_quotes)
        self.stats.negative_cache_hits = negative_cache_hits
        self.stats.missing_quotes = len(clean_symbols) - len(final_quotes)

        return final_quotes

    def _from_market_quote(self, market_quote: MarketQuote) -> Quote:
        return Quote(
            symbol=market_quote.symbol,
            price=market_quote.price,
            volume=market_quote.volume,
            previous_close=market_quote.previous_close,
            change_percent=market_quote.change_percent,
        )

    def _load_cache(self) -> dict:
        if not self.cache_file.exists():
            return {}

        try:
            with self.cache_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                return {}

            return data

        except Exception:
            return {}

    def _update_cache(
        self,
        cache: dict,
        quotes: list[Quote],
        timestamp: datetime,
    ) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        timestamp_text = timestamp.isoformat()

        for quote in quotes:
            cache[quote.symbol] = {
                "type": "quote",
                "timestamp": timestamp_text,
                "quote": asdict(quote),
            }

        self._save_cache(cache)

    def _update_negative_cache(
        self,
        cache: dict,
        symbols: list[str],
        timestamp: datetime,
    ) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        timestamp_text = timestamp.isoformat()

        for symbol in symbols:
            cache[symbol] = {
                "type": "missing",
                "timestamp": timestamp_text,
            }

        self._save_cache(cache)

    def _save_cache(self, cache: dict) -> None:
        try:
            with self.cache_file.open("w", encoding="utf-8") as file:
                json.dump(cache, file, indent=2)

        except Exception:
            return

    def _get_cached_quote(
        self,
        cache: dict,
        symbol: str,
        now: datetime,
    ) -> Quote | None:
        entry = cache.get(symbol)

        if not isinstance(entry, dict):
            return None

        entry_type = entry.get("type", "quote")

        if entry_type != "quote":
            return None

        timestamp_text = entry.get("timestamp")
        quote_data = entry.get("quote")

        if not timestamp_text or not isinstance(quote_data, dict):
            return None

        try:
            timestamp = datetime.fromisoformat(timestamp_text)
        except Exception:
            return None

        if now - timestamp > self.cache_ttl:
            return None

        try:
            return Quote(
                symbol=str(quote_data["symbol"]),
                price=float(quote_data["price"]),
                volume=int(quote_data["volume"]),
                previous_close=(
                    float(quote_data["previous_close"])
                    if quote_data.get("previous_close") is not None
                    else None
                ),
                change_percent=(
                    float(quote_data["change_percent"])
                    if quote_data.get("change_percent") is not None
                    else None
                ),
            )
        except Exception:
            return None

    def _is_negative_cached(
        self,
        cache: dict,
        symbol: str,
        now: datetime,
    ) -> bool:
        entry = cache.get(symbol)

        if not isinstance(entry, dict):
            return False

        if entry.get("type") != "missing":
            return False

        timestamp_text = entry.get("timestamp")

        if not timestamp_text:
            return False

        try:
            timestamp = datetime.fromisoformat(timestamp_text)
        except Exception:
            return False

        return now - timestamp <= self.negative_cache_ttl

    def _clean_symbols(self, symbols: list[str]) -> list[str]:
        clean: list[str] = []
        seen: set[str] = set()

        for symbol in symbols:
            value = str(symbol).strip().upper()

            if not value:
                continue

            if value in seen:
                continue

            seen.add(value)
            clean.append(value)

        return clean