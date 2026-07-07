from __future__ import annotations

from pathlib import Path

import pandas as pd

from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner


class FakeYahooProvider:
    def get_historical_data(
        self,
        symbol: str,
        period: str = "3mo",
        interval: str = "1d",
    ) -> pd.DataFrame:
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


def main():
    print("\n=========================================")
    print("ORION LIVE PAPER MARKET SCANNER TEST")
    print("=========================================\n")

    config = LivePaperTradingConfig(
        watchlist_path=Path("config/watchlist.txt"),
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
    assert result.failed_symbols == 0
    assert len(result.candidates) == 5

    assert result.session.cash >= 0.0
    assert result.session.equity >= 0.0
    assert result.session.open_positions <= 3

    assert result.executed_trades >= 0
    assert result.rejected_trades >= 0
    assert result.executed_trades == 0
    assert result.rejected_trades == 0
    assert len(result.ranked_candidates) == 5

    best = result.best_candidate

    assert best is not None
    assert best.symbol
    assert best.score >= 0.0

    print("LIVE PAPER MARKET SCANNER: PASS ✅")


if __name__ == "__main__":
    main()