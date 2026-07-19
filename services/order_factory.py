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
            currency=context.request.currency,
            fx_rate_to_base=context.request.fx_rate_to_base,
            stop_loss_price=(
                context.request.risk_plan.stop_loss
                if side == "BUY"
                else None
            ),
            take_profit_price=(
                context.request.risk_plan.target_1
                if side == "BUY"
                else None
            ),
            client_order_id=context.request.trade_id,
            oca_group=(
                f"ORION-{context.request.trade_id}"
                if context.request.trade_id
                else ""
            ),
            execution_urgency=context.request.execution_urgency,
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
