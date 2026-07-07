from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.order import Order


@dataclass(frozen=True)
class ExecutionResult:
    accepted: bool
    status: str
    order: Order | None
    message: str
    executed_price: float = 0.0
    executed_quantity: int = 0
    executed_at: datetime | None = None