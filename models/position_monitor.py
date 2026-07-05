from __future__ import annotations

from dataclasses import dataclass

from models.trade_lifecycle import ExitSignal, Trade


@dataclass(frozen=True)
class PositionMonitorResult:
    """
    Deterministic result of monitoring one open trade.

    The result contains no UI logic and no AI output.
    """

    trade: Trade
    exit_signal: ExitSignal
    reason: str

    market_value: float
    invested_amount: float
    unrealized_profit_loss: float
    unrealized_profit_loss_percent: float

    stop_loss_distance: float
    take_profit_distance: float