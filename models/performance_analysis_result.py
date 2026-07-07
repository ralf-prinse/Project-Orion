from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceAnalysisResult:
    """
    Immutable performance analysis result.

    This is ORION's self-evaluation summary over a collection
    of trade journal entries.
    """

    total_trades: int

    winning_trades: int
    losing_trades: int

    win_rate: float

    total_realized_profit_loss: float
    total_unrealized_profit_loss: float

    average_realized_profit_loss: float
    average_return_percent: float

    best_trade_symbol: str | None
    best_trade_return_percent: float

    worst_trade_symbol: str | None
    worst_trade_return_percent: float

    average_confidence: float
    average_expected_risk: float

    profitable_confidence_threshold: float | None

    dominant_regime: str | None
    dominant_volatility: str | None

    summary: str