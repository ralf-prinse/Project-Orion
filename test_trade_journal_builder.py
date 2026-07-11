from __future__ import annotations

from pathlib import Path

import pandas as pd

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import (
    LivePaperTradingConfig,
)
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.live_paper_market_scanner import (
    LivePaperMarketScanner,
)
from services.trade_journal_builder import (
    TradeJournalBuilder,
)


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
        watchlist_path=Path(
            "config/watchlist.txt"
        ),
        initial_cash=500.0,
        max_symbols=3,
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
        cycles=1,
        sleep_seconds=0.0,
        stop_on_exception=True,
        print_cycle_summary=False,
    )

    runner = AutonomousPaperTradingRunner(
        config=config,
        scanner=scanner,
    )

    result = runner.run()
    builder = TradeJournalBuilder()

    entries = builder.build_decision_entries(
        result=result,
        session_id="test-session",
    )

    assert entries
    assert len(entries) == len(
        result
        .cycle_results[0]
        .allocation
        .decisions
    )

    first = entries[0]

    assert first.session_id == "test-session"
    assert first.cycle_number == 1
    assert first.symbol
    assert first.action in {
        "APPROVED",
        "REJECTED",
    }
    assert first.decision in {
        "BUY",
        "HOLD",
        "SELL",
    }
    assert first.confidence >= 0.0
    assert first.score >= 0.0
    assert first.entry_price > 0.0
    assert first.quantity >= 0
    assert first.invested_amount >= 0.0
    assert first.expected_risk >= 0.0
    assert first.regime
    assert first.volatility

    print(
        "TRADE JOURNAL BUILDER: PASS"
    )


if __name__ == "__main__":
    main()
