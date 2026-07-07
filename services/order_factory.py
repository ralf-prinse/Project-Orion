from __future__ import annotations

from datetime import datetime

from models.execution_context import ExecutionContext
from models.order import Order


class OrderFactory:
    """
    Creates deterministic broker-neutral orders.
    """

    def create(
        self,
        context: ExecutionContext,
    ) -> Order:

        return Order(
            symbol=context.symbol,
            side="BUY",
            quantity=context.request.quantity,
            order_type="MARKET",
            price=context.request.entry_price,
            created_at=datetime.now(),
            source="ExecutionEngine",
        )