from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClosedTradeStatistics:
    """
    Deterministic statistics for closed trades.

    This model contains calculated analytics only.
    Business logic belongs in ClosedTradeAnalyticsService.
    """

    closed_trades: int
    winning_trades: int
    losing_trades: int
    winrate_percent: float
    closed_profit_loss: float
    average_winner: float
    average_loser: float
    profit_factor: float
    largest_winner: float
    largest_loser: float