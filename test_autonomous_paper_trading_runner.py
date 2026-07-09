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
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
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
    journal_path = Path("data/test_autonomous_trade_journal.jsonl")

    if journal_path.exists():
        journal_path.unlink()

    live_config = LivePaperTradingConfig(
        watchlist_path=Path("data/universes/swing.csv"),
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

    trade_journal_repository = JsonlTradeJournalRepository(
        path=journal_path,
    )

    runner = AutonomousPaperTradingRunner(
        config=config,
        scanner=scanner,
        trade_journal_repository=trade_journal_repository,
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

    assert journal_path.exists()

    journal_entries = trade_journal_repository.load_all()

    expected_entries = sum(
        len(cycle.allocation.decisions)
        for cycle in result.cycle_results
    )

    assert len(journal_entries) == expected_entries

    first_entry = journal_entries[0]

    assert first_entry.session_id.startswith("autonomous-")
    assert first_entry.symbol
    assert first_entry.action in {"OPEN_POSITION", "REJECTED"}
    assert first_entry.decision in {"BUY", "HOLD", "SELL"}

    trade_journal_repository.delete()

    print("AUTONOMOUS PAPER TRADING RUNNER: PASS ✅")


if __name__ == "__main__":
    main()