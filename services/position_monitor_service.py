from models.position_monitor import PositionMonitorResult
from models.trade_lifecycle import ExitSignal, Trade


class PositionMonitorService:
    """
    Deterministic service for monitoring an open trade.

    This service does not use AI.
    This service does not execute trades.
    """

    def evaluate(self, trade: Trade) -> PositionMonitorResult:
        invested_amount = round(trade.quantity * trade.entry_price, 2)
        market_value = round(trade.quantity * trade.current_price, 2)
        unrealized_profit_loss = round(market_value - invested_amount, 2)

        if invested_amount > 0:
            unrealized_profit_loss_percent = round(
                (unrealized_profit_loss / invested_amount) * 100,
                2,
            )
        else:
            unrealized_profit_loss_percent = 0.0

        exit_signal, reason = self._determine_exit_signal(trade)

        stop_loss_distance = round(trade.current_price - trade.stop_loss, 2)
        take_profit_distance = round(trade.take_profit - trade.current_price, 2)

        return PositionMonitorResult(
            trade=trade,
            exit_signal=exit_signal,
            reason=reason,
            market_value=market_value,
            invested_amount=invested_amount,
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_profit_loss_percent=unrealized_profit_loss_percent,
            stop_loss_distance=stop_loss_distance,
            take_profit_distance=take_profit_distance,
        )

    def _determine_exit_signal(self, trade: Trade) -> tuple[ExitSignal, str]:
        if trade.stop_loss > 0 and trade.current_price <= trade.stop_loss:
            return (
                ExitSignal.STOP_LOSS,
                "De koers staat op of onder je stop-loss. Orion adviseert verkopen om het verlies te beperken.",
            )

        if trade.take_profit > 0 and trade.current_price >= trade.take_profit:
            return (
                ExitSignal.TAKE_PROFIT,
                "De koers heeft je winstdoel bereikt. Orion adviseert winst nemen.",
            )

        return (
            ExitSignal.HOLD_POSITION,
            "Stop-loss en winstdoel zijn nog niet geraakt. Orion adviseert de positie vast te houden.",
        )