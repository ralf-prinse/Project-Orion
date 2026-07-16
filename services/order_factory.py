from __future__ import annotations

from datetime import datetime

from models.execution_context import ExecutionContext
from models.order import Order


class OrderFactory:
    """
    Creates deterministic broker-neutral orders.

    Execution actions are translated to broker-neutral order sides:

    - OPEN_POSITION -> BUY
    - BUY -> BUY
    - CLOSE_POSITION -> SELL
    - SELL -> SELL

    The factory contains no broker-specific implementation and does not
    mutate portfolio or TradingSession state.
    """

    BUY_ACTIONS = {
        "OPEN_POSITION",
        "BUY",
    }

    SELL_ACTIONS = {
        "CLOSE_POSITION",
        "SELL",
    }

    def create(
        self,
        context: ExecutionContext,
    ) -> Order:
        side = self._resolve_side(
            context.request.action,
        )

        return Order(
            symbol=context.symbol,
            side=side,
            quantity=context.request.quantity,
            order_type="MARKET",
            price=context.request.entry_price,
            created_at=datetime.now(),
            source="ExecutionEngine",
        )

    def _resolve_side(
        self,
        action: str,
    ) -> str:
        normalized_action = action.strip().upper()

        if normalized_action in self.BUY_ACTIONS:
            return "BUY"

        if normalized_action in self.SELL_ACTIONS:
            return "SELL"

        raise ValueError(
            "Unsupported execution action: "
            f"{action!r}. "
            "Expected OPEN_POSITION, BUY, CLOSE_POSITION or SELL."
        )