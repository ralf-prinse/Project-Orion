from __future__ import annotations

from datetime import UTC, datetime

from models.execution_result import ExecutionResult
from models.order import Order


class ShadowBroker:
    """Deterministic broker that can never submit an external order.

    Shadow fills use the scanner's reference price. Adverse slippage,
    commissions and external fees remain explicit in Orion's cost estimator
    and trade journal, so the original market price and all conservative cost
    assumptions remain independently auditable without violating RiskPlan
    price integrity.
    """

    def __init__(self, *, slippage_pct_per_side: float = 0.0005) -> None:
        if not 0 <= slippage_pct_per_side < 1:
            raise ValueError(
                "slippage_pct_per_side must be between zero and one."
            )
        self.slippage_pct_per_side = float(slippage_pct_per_side)

    def execute(self, order: Order) -> ExecutionResult:
        if order.quantity <= 0:
            return self._reject(order, "Order quantity must be positive.")
        if order.price <= 0:
            return self._reject(order, "Order price must be positive.")

        side = order.side.strip().upper()
        if side not in {"BUY", "SELL"}:
            return self._reject(order, f"Unsupported side: {order.side!r}.")

        executed_price = round(order.price, 6)

        return ExecutionResult(
            accepted=True,
            status="SHADOW_FILLED",
            order=order,
            message=(
                "Shadow fill simulated at the reference price; adverse "
                "slippage is reserved by the cost model. No broker quote "
                "requested and no external order submitted."
            ),
            executed_price=executed_price,
            executed_quantity=order.quantity,
            executed_at=datetime.now(UTC),
        )

    def _reject(self, order: Order, message: str) -> ExecutionResult:
        return ExecutionResult(
            accepted=False,
            status="SHADOW_REJECTED",
            order=order,
            message=message,
        )
