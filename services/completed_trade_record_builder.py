from __future__ import annotations

from datetime import UTC, datetime

from models.completed_trade_record import CompletedTradeRecord
from models.trade_journal_entry import TradeJournalEntry


class CompletedTradeRecordBuilder:
    """Joins an OPEN/ADOPT journal entry to its confirmed final exit."""

    ENTRY_ACTIONS = {"OPEN_POSITION", "ADOPT_POSITION"}

    def build(
        self,
        *,
        entry: TradeJournalEntry,
        exit: TradeJournalEntry,
    ) -> CompletedTradeRecord:
        if entry.action not in self.ENTRY_ACTIONS:
            raise ValueError("Entry journal action is not OPEN or ADOPT.")
        if exit.action != "CLOSE_POSITION":
            raise ValueError("Exit journal action is not CLOSE_POSITION.")
        if not entry.trade_id or entry.trade_id != exit.trade_id:
            raise ValueError("Entry and exit trade_id must match.")
        if entry.symbol != exit.symbol:
            raise ValueError("Entry and exit symbols must match.")
        if exit.exit_price is None:
            raise ValueError("A completed trade requires an exit price.")

        adopted = entry.action == "ADOPT_POSITION"
        return CompletedTradeRecord(
            trade_id=entry.trade_id,
            symbol=entry.symbol,
            strategy_name=entry.strategy_name,
            opened_at=entry.timestamp,
            closed_at=exit.timestamp,
            quantity=exit.quantity,
            entry_price=entry.entry_price,
            exit_price=exit.exit_price,
            invested_amount=exit.invested_amount,
            gross_profit_loss=exit.realized_profit_loss,
            estimated_trading_costs=exit.estimated_trading_costs,
            estimated_net_profit_loss=exit.estimated_net_profit_loss,
            profit_calculation_currency=exit.profit_calculation_currency,
            holding_seconds=self._holding_seconds(
                entry.timestamp,
                exit.timestamp,
            ),
            entry_decision=entry.decision,
            entry_confidence=entry.confidence,
            entry_score=entry.score,
            entry_regime=entry.regime,
            entry_volatility=entry.volatility,
            entry_summary=entry.ai_summary,
            entry_reason=entry.recommendation_reason,
            exit_decision=exit.decision,
            exit_reason=exit.recommendation_reason,
            adopted_position=adopted,
            original_entry_rationale_available=not adopted,
            entry_news_status=entry.news_status,
            entry_news_risk_level=entry.news_risk_level,
            entry_news_sentiment_score=entry.news_sentiment_score,
            entry_news_event_ids=entry.news_event_ids,
            exit_news_status=exit.news_status,
            exit_news_risk_level=exit.news_risk_level,
            exit_news_sentiment_score=exit.news_sentiment_score,
            exit_news_event_ids=exit.news_event_ids,
        )

    def _holding_seconds(self, opened_at: datetime, closed_at: datetime) -> float:
        def utc(value: datetime) -> datetime:
            if value.tzinfo is None:
                return value.replace(tzinfo=UTC)
            return value.astimezone(UTC)

        return max(0.0, (utc(closed_at) - utc(opened_at)).total_seconds())
