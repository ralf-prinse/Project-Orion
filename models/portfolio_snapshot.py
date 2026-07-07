from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PortfolioSnapshot:
    cash: float
    equity: float
    positions_value: float
    open_positions: int
    realized_profit_loss: float
    unrealized_profit_loss: float
    created_at: datetime