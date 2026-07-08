from pathlib import Path

from models.trade_journal_entry import TradeJournalEntry
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)


def build_entry(
    symbol: str,
) -> TradeJournalEntry:
    return TradeJournalEntry(
        symbol=symbol,
        action="BUY",
        quantity=1,
        entry_price=100.0,
        exit_price=None,
        realized_profit_loss=0.0,
        return_percent=0.0,
        confidence=0.90,
        regime="BULL",
        volatility="LOW",
        notes="Repository regression test.",
    )


def test_append_and_load_entries():
    repository = JsonlTradeJournalRepository(
        path=Path("output/test_trade_journal.jsonl"),
    )

    repository.delete()

    repository.append(
        build_entry("AAPL"),
    )

    repository.append(
        build_entry("MSFT"),
    )

    assert repository.exists()

    entries = repository.load_all()

    assert len(entries) == 2

    assert entries[0].symbol == "AAPL"
    assert entries[1].symbol == "MSFT"

    repository.delete()

    assert repository.exists() is False


def test_load_empty_repository():
    repository = JsonlTradeJournalRepository(
        path=Path("output/test_empty_trade_journal.jsonl"),
    )

    repository.delete()

    assert repository.load_all() == []