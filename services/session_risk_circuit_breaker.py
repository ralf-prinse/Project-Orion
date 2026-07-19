from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from models.completed_trade_record import CompletedTradeRecord
from models.trading_session import TradingSession


@dataclass(frozen=True)
class SessionRiskDecision:
    entries_allowed: bool
    reason: str
    daily_net_profit_loss: float
    consecutive_losses: int


class SessionRiskCircuitBreaker:
    """Deterministic session loss gate; it never blocks managed exits."""

    def evaluate(
        self,
        *,
        session: TradingSession,
        completed_trades: list[CompletedTradeRecord],
        max_daily_loss_pct: float,
        max_consecutive_losses: int,
        cooldown_minutes: int,
        consecutive_order_failures: int = 0,
        max_consecutive_order_failures: int = 3,
        now: datetime | None = None,
    ) -> SessionRiskDecision:
        evaluated_at = now or datetime.now(UTC)
        if evaluated_at.tzinfo is None:
            evaluated_at = evaluated_at.replace(tzinfo=UTC)

        normalized = sorted(
            completed_trades,
            key=lambda record: self._aware(record.closed_at),
        )
        today = evaluated_at.date()
        daily_realized = sum(
            record.estimated_net_profit_loss
            for record in normalized
            if self._aware(record.closed_at).date() == today
        )
        unrealized = sum(
            position.unrealized_profit_loss
            for position in session.portfolio.positions.values()
        )
        daily_net = round(daily_realized + unrealized, 2)
        risk_base = max(
            session.equity,
            session.peak_portfolio_value,
            0.0,
        )
        loss_limit = risk_base * max_daily_loss_pct

        consecutive_losses = 0
        for record in reversed(normalized):
            if record.estimated_net_profit_loss >= 0:
                break
            consecutive_losses += 1

        if daily_net <= -loss_limit and loss_limit > 0:
            return SessionRiskDecision(
                False,
                "Daily realized plus unrealized loss limit reached.",
                daily_net,
                consecutive_losses,
            )

        if consecutive_losses >= max_consecutive_losses and normalized:
            last_close = self._aware(normalized[-1].closed_at)
            cooldown_ends = last_close + timedelta(minutes=cooldown_minutes)
            if evaluated_at < cooldown_ends:
                return SessionRiskDecision(
                    False,
                    "Consecutive-loss cooldown is active until "
                    f"{cooldown_ends.isoformat()}.",
                    daily_net,
                    consecutive_losses,
                )

        if consecutive_order_failures >= max_consecutive_order_failures:
            return SessionRiskDecision(
                False,
                "Consecutive broker execution failure limit reached.",
                daily_net,
                consecutive_losses,
            )

        return SessionRiskDecision(
            True,
            "Session loss controls allow new entries.",
            daily_net,
            consecutive_losses,
        )

    @staticmethod
    def _aware(value: datetime) -> datetime:
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
