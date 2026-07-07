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