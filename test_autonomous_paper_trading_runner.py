from __future__ import annotations

from pathlib import Path

import pandas as pd

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import LivePaperTradingConfig
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
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
    live_config = LivePaperTradingConfig(
        watchlist_path=Path("config/watchlist.txt"),
        initial_cash=500.0,
        max_symbols=5,
        max_open_positions=2,
        min_confidence=0.75,
        max_position_value=150.0,
    )

    scanner = LivePaperMarketScanner(
        config=live_config,
        provider=FakeYahooProvider(),
    )

    config = AutonomousPaperTradingConfig(
        live_config=live_config,
        cycles=2,
        sleep_seconds=0.0,
        stop_on_exception=True,
        print_cycle_summary=False,
    )

    runner = AutonomousPaperTradingRunner(
        config=config,
        scanner=scanner,
    )

    result = runner.run()

    assert result.completed_cycles == 2
    assert result.failed_cycles == 0
    assert len(result.cycle_results) == 2

    assert result.initial_cash == 500.0
    assert result.final_cash >= 0.0
    assert result.final_equity >= 0.0

    assert result.total_executed_trades >= 0
    assert result.total_rejected_trades >= 0
    assert result.total_failed_symbols == 0

    assert result.session.open_positions <= 2

    for cycle in result.cycle_results:
        assert cycle.scan.scanned_symbols == 5
        assert cycle.scan.failed_symbols == 0
        assert cycle.allocation.approved_count >= 0
        assert cycle.allocation.rejected_count >= 0

    print("AUTONOMOUS PAPER TRADING RUNNER: PASS ✅")


if __name__ == "__main__":
    main()