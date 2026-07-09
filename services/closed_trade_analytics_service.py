from __future__ import annotations

from models.closed_trade_statistics import ClosedTradeStatistics
from models.trade_journal_entry import TradeJournalEntry


class ClosedTradeAnalyticsService:
    """
    Deterministic analytics service for closed trades.

    Responsibilities:
    - filter closed trade journal entries
    - calculate closed trade performance statistics

    Does NOT:
    - make trading decisions
    - modify portfolio state
    - load or save data
    - use AI
    """

    CLOSED_ACTION = "CLOSE_POSITION"

    def analyze(
        self,
        journal_entries: list[TradeJournalEntry],
    ) -> ClosedTradeStatistics:
        closed_entries = [
            entry
            for entry in journal_entries
            if entry.action == self.CLOSED_ACTION
        ]

        if not closed_entries:
            return ClosedTradeStatistics(
                closed_trades=0,
                winning_trades=0,
                losing_trades=0,
                winrate_percent=0.0,
                closed_profit_loss=0.0,
                average_winner=0.0,
                average_loser=0.0,
                profit_factor=0.0,
                largest_winner=0.0,
                largest_loser=0.0,
            )

        profits = [
            entry.realized_profit_loss
            for entry in closed_entries
        ]

        winners = [
            profit
            for profit in profits
            if profit > 0
        ]

        losers = [
            profit
            for profit in profits
            if profit < 0
        ]

        closed_trades = len(closed_entries)
        winning_trades = len(winners)
        losing_trades = len(losers)

        gross_profit = sum(winners)
        gross_loss = abs(sum(losers))

        return ClosedTradeStatistics(
            closed_trades=closed_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            winrate_percent=self._percent(
                part=winning_trades,
                total=closed_trades,
            ),
            closed_profit_loss=round(sum(profits), 2),
            average_winner=self._average(winners),
            average_loser=self._average(losers),
            profit_factor=self._profit_factor(
                gross_profit=gross_profit,
                gross_loss=gross_loss,
            ),
            largest_winner=round(max(winners), 2) if winners else 0.0,
            largest_loser=round(min(losers), 2) if losers else 0.0,
        )

    def _average(
        self,
        values: list[float],
    ) -> float:
        if not values:
            return 0.0

        return round(
            sum(values) / len(values),
            2,
        )

    def _percent(
        self,
        part: int,
        total: int,
    ) -> float:
        if total <= 0:
            return 0.0

        return round(
            (part / total) * 100,
            2,
        )

    def _profit_factor(
        self,
        gross_profit: float,
        gross_loss: float,
    ) -> float:
        if gross_loss <= 0:
            return 0.0

        return round(
            gross_profit / gross_loss,
            2,
        )