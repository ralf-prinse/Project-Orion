from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from models.trade_journal_entry import TradeJournalEntry
from models.paper_position import PaperPosition
from services.autonomous_paper_trading_runner import AutonomousPaperTradingRunner
from services.completed_trade_record_builder import CompletedTradeRecordBuilder
from services.stores.jsonl_completed_trade_repository import (
    JsonlCompletedTradeRepository,
)


OPENED = datetime(2026, 7, 19, 8, 0, tzinfo=UTC)


def journal(*, action, timestamp, trade_id="trade-1", exit_price=None):
    return TradeJournalEntry(
        timestamp=timestamp,
        symbol="AAPL",
        action=action,
        decision="BUY" if action == "OPEN_POSITION" else "TAKE_PROFIT",
        confidence=0.88,
        score=0.77,
        entry_price=100.0,
        exit_price=exit_price,
        quantity=2,
        invested_amount=200.0,
        realized_profit_loss=6.0 if exit_price else 0.0,
        unrealized_profit_loss=0.0,
        expected_risk=4.0,
        regime="BULL",
        volatility="LOW",
        ai_summary="Canonical pipeline explanation",
        recommendation_reason=(
            "Signal fusion approved" if exit_price is None else "Net target reached"
        ),
        cycle_number=1,
        session_id="session-1",
        trade_id=trade_id,
        estimated_trading_costs=2.0 if exit_price else 0.0,
        estimated_net_profit_loss=4.0 if exit_price else 0.0,
        news_mode="SHADOW",
        news_status="AVAILABLE",
        news_risk_level="LOW",
        news_sentiment_score=0.25,
        news_event_ids=("news-1",),
    )


def test_completed_record_preserves_entry_exit_news_and_net_result(tmp_path):
    entry = journal(action="OPEN_POSITION", timestamp=OPENED)
    exit_entry = journal(
        action="CLOSE_POSITION",
        timestamp=OPENED + timedelta(hours=3),
        exit_price=103.0,
    )
    record = CompletedTradeRecordBuilder().build(entry=entry, exit=exit_entry)

    assert record.trade_id == "trade-1"
    assert record.entry_reason == "Signal fusion approved"
    assert record.exit_reason == "Net target reached"
    assert record.estimated_net_profit_loss == 4.0
    assert record.holding_seconds == 10_800
    assert record.entry_news_event_ids == ("news-1",)
    assert record.was_profitable_after_estimated_costs is True

    repository = JsonlCompletedTradeRepository(tmp_path / "completed.jsonl")
    assert repository.append_unique(record) is True
    assert repository.append_unique(record) is False
    assert repository.load_all() == [record]


def test_adopted_trade_marks_original_buy_rationale_unavailable():
    entry = journal(action="ADOPT_POSITION", timestamp=OPENED)
    exit_entry = journal(
        action="CLOSE_POSITION",
        timestamp=OPENED + timedelta(minutes=30),
        exit_price=103.0,
    )

    record = CompletedTradeRecordBuilder().build(entry=entry, exit=exit_entry)

    assert record.adopted_position is True
    assert record.original_entry_rationale_available is False


def test_mismatched_trade_ids_are_rejected():
    with pytest.raises(ValueError, match="trade_id"):
        CompletedTradeRecordBuilder().build(
            entry=journal(action="OPEN_POSITION", timestamp=OPENED),
            exit=journal(
                action="CLOSE_POSITION",
                timestamp=OPENED + timedelta(hours=1),
                trade_id="other",
                exit_price=101.0,
            ),
        )


class MemoryJournal:
    def __init__(self, entries):
        self.entries = list(entries)

    def append(self, entry):
        self.entries.append(entry)

    def load_all(self):
        return list(self.entries)


class MemoryCompletedTrades:
    def __init__(self):
        self.records = []

    def append_unique(self, record):
        self.records.append(record)
        return True


def test_runner_persists_completed_record_after_confirmed_local_exit():
    trade_journal = MemoryJournal(
        [journal(action="OPEN_POSITION", timestamp=OPENED)]
    )
    completed = MemoryCompletedTrades()
    runner = AutonomousPaperTradingRunner(
        trade_journal_repository=trade_journal,
        completed_trade_repository=completed,
    )

    runner._append_exit_journal_entry(
        PaperPosition(
            symbol="AAPL",
            quantity=2,
            entry_price=100.0,
            current_price=103.0,
        ),
        "TAKE_PROFIT",
        "Net target reached",
        2,
        "session-1",
        estimated_trading_costs=2.0,
        estimated_net_profit_loss=4.0,
        trade_id="trade-1",
    )

    assert len(completed.records) == 1
    assert completed.records[0].trade_id == "trade-1"
    assert completed.records[0].exit_reason == "Net target reached"
