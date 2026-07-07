from __future__ import annotations

from datetime import datetime

from models.execution_result import ExecutionResult
from models.order import Order


class PaperBroker:
    """
    Simulated broker for paper trading.

    No real orders.
    No external API.
    No live money.
    """

    def execute(
        self,
        order: Order,
    ) -> ExecutionResult:

        if order.quantity <= 0:
            return ExecutionResult(
                accepted=False,
                status="REJECTED",
                order=order,
                message="Order quantity must be greater than zero.",
            )

        if order.price <= 0:
            return ExecutionResult(
                accepted=False,
                status="REJECTED",
                order=order,
                message="Order price must be greater than zero.",
            )

        return ExecutionResult(
            accepted=True,
            status="FILLED",
            order=order,
            message="Paper order filled.",
            executed_price=order.price,
            executed_quantity=order.quantity,
            executed_at=datetime.now(),
        )