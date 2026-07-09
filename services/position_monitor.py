from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition


@dataclass(frozen=True)
class PositionMonitorResult:
    symbol: str
    action: str
    reason: str
    current_price: float
    entry_price: float
    unrealized_profit_loss: float
    unrealized_return_percent: float


class PositionMonitor:
    """
    Evaluates open paper positions against lifecycle exit rules.

    This service only decides what should happen.
    It does not mutate portfolios and does not execute trades.
    """

    def evaluate(
        self,
        position: PaperPosition,
        config: LivePaperTradingConfig,
        opened_at: datetime | None = None,
        now: datetime | None = None,
    ) -> PositionMonitorResult:
        current_price = position.current_price
        entry_price = position.entry_price

        unrealized_profit_loss = round(
            position.market_value - position.cost_basis,
            2,
        )

        unrealized_return_percent = self._return_percent(
            current_price=current_price,
            entry_price=entry_price,
        )

        if unrealized_return_percent >= config.take_profit_percent:
            return self._result(
                position=position,
                action="TAKE_PROFIT",
                reason="Take profit threshold reached.",
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=unrealized_return_percent,
            )

        if unrealized_return_percent <= -config.stop_loss_percent:
            return self._result(
                position=position,
                action="STOP_LOSS",
                reason="Stop loss threshold reached.",
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=unrealized_return_percent,
            )

        if opened_at is not None:
            current_time = now or datetime.now()
            holding_days = (current_time - opened_at).days

            if holding_days >= config.max_holding_days:
                return self._result(
                    position=position,
                    action="MAX_HOLDING_TIME",
                    reason="Maximum holding period reached.",
                    unrealized_profit_loss=unrealized_profit_loss,
                    unrealized_return_percent=unrealized_return_percent,
                )

        return self._result(
            position=position,
            action="HOLD",
            reason="No exit condition reached.",
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )

    def _return_percent(
        self,
        current_price: float,
        entry_price: float,
    ) -> float:
        if entry_price <= 0:
            return 0.0

        return round(
            (current_price - entry_price) / entry_price,
            6,
        )

    def _result(
        self,
        position: PaperPosition,
        action: str,
        reason: str,
        unrealized_profit_loss: float,
        unrealized_return_percent: float,
    ) -> PositionMonitorResult:
        return PositionMonitorResult(
            symbol=position.symbol,
            action=action,
            reason=reason,
            current_price=position.current_price,
            entry_price=position.entry_price,
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )