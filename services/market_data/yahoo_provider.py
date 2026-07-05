from __future__ import annotations

from datetime import datetime
from typing import Iterable
import contextlib
import io
import time

import yfinance as yf

from services.market_data.base_provider import (
    MarketDataProvider,
    MarketDataProviderStats,
    MarketQuote,
)


class YahooMarketDataProvider(MarketDataProvider):
    """
    Yahoo Finance market data provider.

    Deze klasse is de enige plek waar yfinance direct gebruikt wordt
    voor quote-data.
    """

    provider_name = "YahooMarketDataProvider"

    def __init__(self, batch_size: int = 500):
        super().__init__()
        self.batch_size = batch_size

    def get_quotes(self, symbols: list[str]) -> list[MarketQuote]:
        start_time = time.perf_counter()

        clean_symbols = self._clean_symbols(symbols)

        if not clean_symbols:
            self.stats = MarketDataProviderStats(
                provider_name=self.provider_name,
                requested_symbols=0,
                received_quotes=0,
                missing_quotes=0,
                duration_seconds=0.0,
            )
            return []

        quotes: list[MarketQuote] = []

        for batch in self._chunks(clean_symbols, self.batch_size):
            batch_quotes = self._get_batch_quotes(batch)
            quotes.extend(batch_quotes)

        duration = time.perf_counter() - start_time

        self.stats = MarketDataProviderStats(
            provider_name=self.provider_name,
            requested_symbols=len(clean_symbols),
            received_quotes=len(quotes),
            missing_quotes=len(clean_symbols) - len(quotes),
            duration_seconds=duration,
        )

        return quotes

    def _get_batch_quotes(self, symbols: list[str]) -> list[MarketQuote]:
        if not symbols:
            return []

        yf_symbols = [self._to_yfinance_symbol(symbol) for symbol in symbols]
        symbol_map = dict(zip(yf_symbols, symbols))

        try:
            with self._suppress_output():
                data = yf.download(
                    tickers=yf_symbols,
                    period="5d",
                    interval="1d",
                    group_by="ticker",
                    auto_adjust=False,
                    threads=True,
                    progress=False,
                )
        except Exception:
            return []

        quotes: list[MarketQuote] = []

        for yf_symbol in yf_symbols:
            original_symbol = symbol_map[yf_symbol]

            try:
                quote = self._extract_quote(
                    data=data,
                    yf_symbol=yf_symbol,
                    original_symbol=original_symbol,
                    multi_symbol=len(yf_symbols) > 1,
                )

                if quote is not None:
                    quotes.append(quote)

            except Exception:
                continue

        return quotes

    def _extract_quote(
        self,
        data,
        yf_symbol: str,
        original_symbol: str,
        multi_symbol: bool,
    ) -> MarketQuote | None:
        if data is None or data.empty:
            return None

        if multi_symbol:
            if yf_symbol not in data.columns.get_level_values(0):
                return None

            symbol_data = data[yf_symbol].dropna(how="all")
        else:
            symbol_data = data.dropna(how="all")

        if symbol_data.empty:
            return None

        if "Close" not in symbol_data.columns or "Volume" not in symbol_data.columns:
            return None

        valid_rows = symbol_data.dropna(subset=["Close", "Volume"])

        if valid_rows.empty:
            return None

        latest = valid_rows.iloc[-1]
        previous = valid_rows.iloc[-2] if len(valid_rows) >= 2 else None

        price = float(latest["Close"])
        volume = int(latest["Volume"])

        if price <= 0 or volume <= 0:
            return None

        previous_close = None
        change_percent = None

        if previous is not None:
            previous_close = float(previous["Close"])

            if previous_close > 0:
                change_percent = ((price - previous_close) / previous_close) * 100

        return MarketQuote(
            symbol=original_symbol,
            price=price,
            volume=volume,
            previous_close=previous_close,
            change_percent=change_percent,
            data_timestamp=self._extract_data_timestamp(valid_rows),
        )

    def _extract_data_timestamp(self, valid_rows) -> datetime | None:
        if valid_rows is None or valid_rows.empty:
            return None

        latest_index = valid_rows.index[-1]

        if hasattr(latest_index, "to_pydatetime"):
            return latest_index.to_pydatetime()

        if isinstance(latest_index, datetime):
            return latest_index

        return None

    def _clean_symbols(self, symbols: Iterable[str]) -> list[str]:
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

    def _chunks(self, items: list[str], size: int) -> Iterable[list[str]]:
        for index in range(0, len(items), size):
            yield items[index:index + size]

    def _to_yfinance_symbol(self, symbol: str) -> str:
        return symbol.replace(".", "-")

    @contextlib.contextmanager
    def _suppress_output(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with contextlib.redirect_stderr(io.StringIO()):
                yield