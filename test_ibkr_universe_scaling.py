from __future__ import annotations

from pathlib import Path

import pandas as pd
from run_autonomous_ibkr_paper import (
    CYCLES_ENVIRONMENT_VARIABLE,
    SCAN_INTERVAL_ENVIRONMENT_VARIABLE,
    read_cycle_count,
    read_scan_interval_seconds,
)
from services.market_data.historical_cache import HistoricalCache
from services.market_data.yahoo_historical_provider import (
    YahooHistoricalDataProvider,
)


class EmptyCache:
    def get(self, symbol, period, interval):
        return None

    def set(self, symbol, period, interval, data):
        return None


def test_ibkr_validation_universe_contains_fifty_us_and_fifty_eu() -> None:
    symbols = [
        line.strip()
        for line in Path(
            "data/universes/ibkr_eu_us_validation.csv"
        ).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    amsterdam = [symbol for symbol in symbols if symbol.endswith(".AS")]
    germany = [symbol for symbol in symbols if symbol.endswith(".DE")]
    united_states = [
        symbol
        for symbol in symbols
        if not symbol.endswith((".AS", ".DE"))
    ]

    assert len(symbols) == 100
    assert len(set(symbols)) == 100
    assert len(united_states) == 50
    assert len(amsterdam) == 25
    assert len(germany) == 25


def test_yahoo_history_provider_downloads_one_hundred_in_four_batches(
    monkeypatch,
) -> None:
    provider = YahooHistoricalDataProvider(
        cache=EmptyCache(),
        batch_size=25,
    )
    batches = []
    history = pd.DataFrame(
        {
            "Open": [100.0],
            "High": [101.0],
            "Low": [99.0],
            "Close": [100.5],
            "Volume": [1_000_000],
        }
    )

    def fake_download_batch(*, symbols, period, interval):
        batches.append(list(symbols))
        return {symbol: history.copy() for symbol in symbols}

    monkeypatch.setattr(provider, "_download_batch", fake_download_batch)
    symbols = [f"TEST{index:03d}" for index in range(100)]

    result = provider.get_history(
        symbols=symbols,
        period="3mo",
        interval="1d",
    )

    assert [len(batch) for batch in batches] == [25, 25, 25, 25]
    assert set(result) == set(symbols)
    assert provider.stats.fresh_downloads == 100


def test_historical_cache_accepts_fifteen_minute_ttl(tmp_path) -> None:
    cache = HistoricalCache(
        cache_dir=str(tmp_path),
        ttl_minutes=15,
    )

    assert cache.ttl.total_seconds() == 900


def test_bounded_cycle_environment(monkeypatch) -> None:
    monkeypatch.setenv(CYCLES_ENVIRONMENT_VARIABLE, "12")
    monkeypatch.setenv(SCAN_INTERVAL_ENVIRONMENT_VARIABLE, "900")

    assert read_cycle_count() == 12
    assert read_scan_interval_seconds() == 900


def test_yahoo_symbol_normalization_preserves_exchange_suffixes() -> None:
    provider = YahooHistoricalDataProvider(cache=EmptyCache())

    assert provider._to_yfinance_symbol("asml.as") == "ASML.AS"
    assert provider._to_yfinance_symbol("sap.de") == "SAP.DE"
