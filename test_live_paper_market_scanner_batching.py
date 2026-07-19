from __future__ import annotations

from types import SimpleNamespace

import pandas as pd

from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner


class FixedWatchlist:
    def load_symbols(self) -> list[str]:
        return ["AAPL", "MSFT", "ASML.AS", "SAP.DE"]


class SingleSymbolProviderMustNotRun:
    def get_historical_data(self, **kwargs):
        raise AssertionError(
            "Scanner must use the configured batch historical provider."
        )


class FakeBatchHistoricalProvider:
    def __init__(self) -> None:
        self.calls = []

    def get_history(self, symbols, period, interval):
        self.calls.append((list(symbols), period, interval))
        history = pd.DataFrame(
            {
                "Open": [99.0, 100.0],
                "High": [101.0, 102.0],
                "Low": [98.0, 99.0],
                "Close": [100.0, 101.0],
                "Volume": [1_000_000, 1_100_000],
            }
        )
        return {symbol: history.copy() for symbol in symbols}


class FakeAdapter:
    def __init__(self) -> None:
        self.symbols = []

    def run(self, symbol, history, portfolio_state):
        self.symbols.append(symbol)
        return SimpleNamespace(
            symbol=symbol,
            decision="HOLD",
            confidence=0.8,
            expected_risk=0.01,
            risk_plan=SimpleNamespace(entry_price=101.0),
            market_intelligence=None,
            explanation="Batch scanner test.",
        )


class FakeRankingEngine:
    def rank(self, result):
        return SimpleNamespace(score=50.0)


def test_scanner_prefetches_all_symbols_in_one_provider_call() -> None:
    batch_provider = FakeBatchHistoricalProvider()
    adapter = FakeAdapter()
    scanner = LivePaperMarketScanner(
        config=LivePaperTradingConfig(max_symbols=100),
        provider=SingleSymbolProviderMustNotRun(),
        historical_provider=batch_provider,
        watchlist_service=FixedWatchlist(),
        adapter=adapter,
        ranking_engine=FakeRankingEngine(),
    )

    result = scanner.run()

    assert batch_provider.calls == [
        (["AAPL", "MSFT", "ASML.AS", "SAP.DE"], "3mo", "1d")
    ]
    assert adapter.symbols == ["AAPL", "MSFT", "ASML.AS", "SAP.DE"]
    assert result.scanned_symbols == 4
    assert result.succeeded_symbols == 4
    assert result.failed_symbols == 0
    assert len(result.candidates) == 4
