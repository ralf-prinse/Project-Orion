from pathlib import Path
from datetime import UTC, datetime

from models.trade_journal_entry import TradeJournalEntry
from services.stores.jsonl_trade_journal_repository import (
    JsonlTradeJournalRepository,
)


def build_entry(
    symbol: str,
) -> TradeJournalEntry:
    return TradeJournalEntry(
        timestamp=datetime(2026, 7, 19, tzinfo=UTC),
        symbol=symbol,
        action="OPEN_POSITION",
        decision="BUY",
        confidence=0.90,
        score=90.0,
        entry_price=100.0,
        exit_price=None,
        quantity=1,
        invested_amount=100.0,
        realized_profit_loss=0.0,
        unrealized_profit_loss=0.0,
        expected_risk=4.0,
        regime="BULL",
        volatility="LOW",
        ai_summary="Repository regression test.",
        recommendation_reason="Approved allocation.",
        cycle_number=1,
        session_id="repository-test",
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
    assert entries[0].timestamp == datetime(2026, 7, 19, tzinfo=UTC)

    repository.delete()

    assert repository.exists() is False


def test_load_empty_repository():
    repository = JsonlTradeJournalRepository(
        path=Path("output/test_empty_trade_journal.jsonl"),
    )

    repository.delete()

    assert repository.load_all() == []
