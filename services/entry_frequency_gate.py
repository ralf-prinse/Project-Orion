from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from models.completed_trade_record import CompletedTradeRecord
from models.trading_session import TradingSession


@dataclass(frozen=True)
class EntryFrequencyDecision:
    allowed: bool
    reason: str
    entries_today: int


class EntryFrequencyGate:
    """Limits daily entries and rapid re-entry after a completed trade."""

    def evaluate(
        self,
        *,
        symbol: str,
        session: TradingSession,
        completed_trades: list[CompletedTradeRecord],
        max_new_positions_per_day: int,
        reentry_cooldown_minutes: int,
        now: datetime | None = None,
    ) -> EntryFrequencyDecision:
        evaluated_at = self._as_utc(now or datetime.now(UTC))
        trade_date = evaluated_at.date()
        entry_ids: set[str] = set()

        for state in session.position_states.values():
            if self._as_utc(state.opened_at).date() == trade_date:
                entry_ids.add(state.trade_id or f"open:{state.symbol}")

        for trade in completed_trades:
            if self._as_utc(trade.opened_at).date() == trade_date:
                entry_ids.add(trade.trade_id)

        entries_today = len(entry_ids)
        if entries_today >= max_new_positions_per_day:
            return EntryFrequencyDecision(
                allowed=False,
                reason=(
                    "Daily entry limit reached: "
                    f"{entries_today}/{max_new_positions_per_day}."
                ),
                entries_today=entries_today,
            )

        normalized_symbol = str(symbol).strip().upper()
        matching_closes = [
            self._as_utc(trade.closed_at)
            for trade in completed_trades
            if str(trade.symbol).strip().upper() == normalized_symbol
        ]
        if matching_closes and reentry_cooldown_minutes > 0:
            latest_close = max(matching_closes)
            cooldown_ends = latest_close + timedelta(
                minutes=reentry_cooldown_minutes
            )
            if evaluated_at < cooldown_ends:
                return EntryFrequencyDecision(
                    allowed=False,
                    reason=(
                        "Re-entry cooldown is active until "
                        f"{cooldown_ends.isoformat()}."
                    ),
                    entries_today=entries_today,
                )

        return EntryFrequencyDecision(
            allowed=True,
            reason="Entry frequency limits passed.",
            entries_today=entries_today,
        )

    def _as_utc(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
