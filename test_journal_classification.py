from __future__ import annotations

from pathlib import Path

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import (
    LivePaperTradingConfig,
)
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)


TRADE_PATH = Path(
    "output/test_classified_trade_journal.jsonl"
)
DECISION_PATH = Path(
    "output/test_classified_decision_journal.jsonl"
)


class EmptyScanner:
    def run(self, session):
        return type(
            "ScanResult",
            (),
            {
                "candidates": [],
                "scanned_symbols": 0,
            },
        )()


def test_empty_cycle_writes_no_journal_entries():
    trade_repository = (
        JsonlTradeJournalRepository(
            path=TRADE_PATH,
        )
    )
    decision_repository = (
        JsonlTradeJournalRepository(
            path=DECISION_PATH,
        )
    )

    trade_repository.delete()
    decision_repository.delete()

    runner = AutonomousPaperTradingRunner(
        config=AutonomousPaperTradingConfig(
            cycles=1,
            sleep_seconds=0,
            live_config=(
                LivePaperTradingConfig(
                    initial_cash=500.0,
                    max_symbols=1,
                )
            ),
            print_cycle_summary=False,
        ),
        scanner=EmptyScanner(),
        trade_journal_repository=(
            trade_repository
        ),
        decision_journal_repository=(
            decision_repository
        ),
    )

    result = runner.run()

    assert result.failed_cycles == 0
    assert trade_repository.load_all() == []
    assert decision_repository.load_all() == []

    trade_repository.delete()
    decision_repository.delete()


def main():
    print()
    print("=========================================")
    print("JOURNAL CLASSIFICATION TEST")
    print("=========================================")
    print()

    test_empty_cycle_writes_no_journal_entries()

    print("JOURNAL CLASSIFICATION: PASS")


if __name__ == "__main__":
    main()
