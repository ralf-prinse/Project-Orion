from __future__ import annotations

from pathlib import Path

import pandas as pd

from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner


class FakeYahooProvider:
    def __init__(
        self,
        failing_symbols: set[str] | None = None,
    ):
        self.failing_symbols = failing_symbols or set()

    def get_historical_data(
        self,
        symbol: str,
        period: str = "3mo",
        interval: str = "1d",
    ) -> pd.DataFrame:
        if symbol in self.failing_symbols:
            raise ValueError(f"Fake provider failure for {symbol}")

        rows = []

        for index in range(80):
            close = 100.0 + index

            rows.append(
                {
                    "Open": close - 0.5,
                    "High": close + 1.0,
                    "Low": close - 1.0,
                    "Close": close,
                    "Volume": 1000 + index,
                }
            )

        return pd.DataFrame(rows)


def test_successful_scan():
    config = LivePaperTradingConfig(
        watchlist_path=Path("data/universes/swing.csv"),
        initial_cash=500.0,
        max_symbols=5,
        max_open_positions=3,
        min_confidence=0.75,
        max_position_value=150.0,
    )

    scanner = LivePaperMarketScanner(
        config=config,
        provider=FakeYahooProvider(),
    )

    result = scanner.run()

    assert result.scanned_symbols == 5
    assert result.succeeded_symbols == 5
    assert result.failed_symbols == 0
    assert result.failed_symbol_errors == {}
    assert result.scan_duration_seconds >= 0.0
    assert len(result.candidates) == 5

    assert result.session.cash >= 0.0
    assert result.session.equity >= 0.0
    assert result.session.open_positions <= 3

    assert result.executed_trades == 0
    assert result.rejected_trades == 0
    assert len(result.ranked_candidates) == 5

    best = result.best_candidate

    assert best is not None
    assert best.symbol
    assert best.score >= 0.0


def test_failed_symbol_is_reported():
    config = LivePaperTradingConfig(
        watchlist_path=Path("data/universes/swing.csv"),
        initial_cash=500.0,
        max_symbols=5,
        max_open_positions=3,
        min_confidence=0.75,
        max_position_value=150.0,
    )

    scanner = LivePaperMarketScanner(
        config=config,
        provider=FakeYahooProvider(
            failing_symbols={"AAPL"},
        ),
    )

    result = scanner.run()

    assert result.scanned_symbols == 5
    assert result.succeeded_symbols == 4
    assert result.failed_symbols == 1
    assert "AAPL" in result.failed_symbol_errors
    assert result.failed_symbol_errors["AAPL"] == (
        "Fake provider failure for AAPL"
    )
    assert len(result.candidates) == 4


def main():
    print("\n=========================================")
    print("ORION LIVE PAPER MARKET SCANNER TEST")
    print("=========================================\n")

    test_successful_scan()
    test_failed_symbol_is_reported()

    print("LIVE PAPER MARKET SCANNER: PASS ✅")


if __name__ == "__main__":
    main()