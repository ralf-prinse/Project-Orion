from __future__ import annotations

from dataclasses import dataclass, field

from models.trade_lifecycle import ExitSignal, Trade


@dataclass(frozen=True)
class PositionMonitorResult:
    """
    Deterministic result of monitoring one open trade.

    Dit object bevat uitsluitend businessdata.
    Geen UI.
    Geen AI.
    Geen formattering.
    """

    # ------------------------------
    # Trade
    # ------------------------------

    trade: Trade

    # ------------------------------
    # Exit beslissing
    # ------------------------------

    exit_signal: ExitSignal

    exit_score: int

    reason: str

    exit_reasons: list[str] = field(default_factory=list)

    # ------------------------------
    # Gezondheid van de trade
    # ------------------------------

    trend_status: str = ""

    momentum_status: str = ""

    risk_status: str = ""

    # ------------------------------
    # Financieel
    # ------------------------------

    market_value: float = 0.0

    invested_amount: float = 0.0

    unrealized_profit_loss: float = 0.0

    unrealized_profit_loss_percent: float = 0.0

    stop_loss_distance: float = 0.0

    take_profit_distance: float = 0.0