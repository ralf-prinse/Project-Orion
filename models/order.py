from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Order:
    symbol: str
    side: str
    quantity: int
    order_type: str
    price: float
    created_at: datetime
    source: str = "ExecutionEngine"
    currency: str = "EUR"
    fx_rate_to_base: float = 1.0
    stop_loss_price: float | None = None
    take_profit_price: float | None = None
    client_order_id: str = ""
    oca_group: str = ""
    execution_urgency: str = "NORMAL"
