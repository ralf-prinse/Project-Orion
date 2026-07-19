import time

import pandas as pd
import yfinance as yf

from services.market_data.historical_cache import HistoricalCache
from services.market_data.historical_provider import (
    HistoricalDataProvider,
    HistoricalProviderStats,
)


class YahooHistoricalDataProvider(HistoricalDataProvider):
    """
    Yahoo-implementatie voor historische candles.

    Dit is de enige plek waar yfinance gebruikt mag worden voor historische data.
    """

    def __init__(
        self,
        cache: HistoricalCache | None = None,
        batch_size: int = 100,
    ):
        super().__init__()
        self.cache = cache or HistoricalCache()
        self.batch_size = batch_size

    def get_history(
        self,
        symbols: list[str],
        period: str = "6mo",
        interval: str = "1d",
    ) -> dict[str, pd.DataFrame]:
        start = time.perf_counter()

        self.stats = HistoricalProviderStats(
            provider_name=self.__class__.__name__,
            requested_symbols=len(symbols),
        )

        if not symbols:
            self.stats.duration_seconds = time.perf_counter() - start
            return {}

        history: dict[str, pd.DataFrame] = {}
        symbols_to_download: list[str] = []

        for symbol in symbols:
            cached_data = self.cache.get(
                symbol=symbol,
                period=period,
                interval=interval,
            )

            if cached_data is not None and not cached_data.empty:
                history[symbol] = cached_data
                self.stats.cache_hits += 1
            else:
                symbols_to_download.append(symbol)

        for symbol_batch in self._chunks(symbols_to_download, self.batch_size):
            downloaded = self._download_batch(
                symbols=symbol_batch,
                period=period,
                interval=interval,
            )

            for symbol, data in downloaded.items():
                if data is None or data.empty:
                    continue

                history[symbol] = data
                self.cache.set(
                    symbol=symbol,
                    period=period,
                    interval=interval,
                    data=data,
                )
                self.stats.fresh_downloads += 1

        self.stats.received_symbols = len(history)
        self.stats.missing_symbols = max(0, len(symbols) - len(history))
        self.stats.duration_seconds = time.perf_counter() - start

        return history

    def _download_batch(
        self,
        symbols: list[str],
        period: str,
        interval: str,
    ) -> dict[str, pd.DataFrame]:
        if not symbols:
            return {}

        yf_symbols = [self._to_yfinance_symbol(symbol) for symbol in symbols]
        yf_to_original = {
            self._to_yfinance_symbol(symbol): symbol
            for symbol in symbols
        }

        try:
            data = yf.download(
                tickers=yf_symbols,
                period=period,
                interval=interval,
                group_by="ticker",
                auto_adjust=True,
                progress=False,
                threads=True,
            )
        except Exception:
            return {}

        if data is None or data.empty:
            return {}

        result: dict[str, pd.DataFrame] = {}

        multi_symbol = len(yf_symbols) > 1

        for yf_symbol in yf_symbols:
            original_symbol = yf_to_original.get(yf_symbol)

            if original_symbol is None:
                continue

            symbol_data = self._extract_symbol_data(
                data=data,
                yf_symbol=yf_symbol,
                multi_symbol=multi_symbol,
            )

            if symbol_data is None or symbol_data.empty:
                continue

            result[original_symbol] = symbol_data.dropna(how="all")

        return result

    def _extract_symbol_data(
        self,
        data: pd.DataFrame,
        yf_symbol: str,
        multi_symbol: bool,
    ) -> pd.DataFrame | None:
        if multi_symbol:
            if not isinstance(data.columns, pd.MultiIndex):
                return None

            if yf_symbol not in data.columns.get_level_values(0):
                return None

            return data[yf_symbol].dropna(how="all")

        return data.dropna(how="all")

    def _chunks(self, items: list[str], size: int):
        for index in range(0, len(items), size):
            yield items[index:index + size]

    def _to_yfinance_symbol(self, symbol: str) -> str:
        return str(symbol).strip().upper()
