from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan


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
    def evaluate(
        self,
        position: PaperPosition,
        config: LivePaperTradingConfig,
        opened_at: datetime | None = None,
        now: datetime | None = None,
    ) -> PositionMonitorResult:
        unrealized_profit_loss = self._unrealized_profit_loss(position)
        unrealized_return_percent = self._return_percent(
            current_price=position.current_price,
            entry_price=position.entry_price,
        )

        if unrealized_return_percent >= config.take_profit_percent:
            return self._result(
                position,
                "TAKE_PROFIT",
                "Take profit threshold reached.",
                unrealized_profit_loss,
                unrealized_return_percent,
            )

        if unrealized_return_percent <= -config.stop_loss_percent:
            return self._result(
                position,
                "STOP_LOSS",
                "Stop loss threshold reached.",
                unrealized_profit_loss,
                unrealized_return_percent,
            )

        if opened_at is not None:
            holding_days = ((now or datetime.now()) - opened_at).days
            if holding_days >= config.max_holding_days:
                return self._result(
                    position,
                    "MAX_HOLDING_TIME",
                    "Maximum holding period reached.",
                    unrealized_profit_loss,
                    unrealized_return_percent,
                )

        return self._result(
            position,
            "HOLD",
            "No exit condition reached.",
            unrealized_profit_loss,
            unrealized_return_percent,
        )

    def evaluate_managed(
        self,
        position: PaperPosition,
        state: PositionState,
        risk_plan: RiskPlan,
    ) -> PositionMonitorResult:
        self._validate_managed_inputs(position, state, risk_plan)
        unrealized_profit_loss = self._unrealized_profit_loss(position)
        unrealized_return_percent = self._return_percent(
            current_price=position.current_price,
            entry_price=position.entry_price,
        )

        if position.current_price <= state.current_stop_loss:
            return self._result(
                position,
                "STOP_LOSS",
                self._managed_stop_reason(state),
                unrealized_profit_loss,
                unrealized_return_percent,
            )

        if position.current_price >= risk_plan.target_3:
            return self._result(
                position,
                "TAKE_PROFIT",
                "Final profit target reached.",
                unrealized_profit_loss,
                unrealized_return_percent,
            )

        return self._result(
            position,
            "HOLD",
            "No lifecycle exit condition reached.",
            unrealized_profit_loss,
            unrealized_return_percent,
        )

    def _validate_managed_inputs(
        self,
        position: PaperPosition,
        state: PositionState,
        risk_plan: RiskPlan,
    ) -> None:
        position_symbol = self._normalize_symbol(position.symbol)
        if not position_symbol:
            raise ValueError("Managed position symbol is required.")
        if position_symbol != self._normalize_symbol(state.symbol):
            raise ValueError(
                "PositionState symbol does not match PaperPosition symbol."
            )
        if position_symbol != self._normalize_symbol(risk_plan.symbol):
            raise ValueError(
                "RiskPlan symbol does not match PaperPosition symbol."
            )
        if position.entry_price <= 0:
            raise ValueError(
                "Managed position entry price must be greater than zero."
            )
        if state.current_stop_loss <= 0:
            raise ValueError(
                "Managed position stop loss must be greater than zero."
            )
        if risk_plan.target_3 <= 0:
            raise ValueError(
                "Managed position final target must be greater than zero."
            )

    def _managed_stop_reason(self, state: PositionState) -> str:
        if state.trailing_stop_active:
            return "Dynamic trailing stop reached."
        if state.break_even_active:
            return "Break-even stop reached."
        return "Initial lifecycle stop reached."

    def _unrealized_profit_loss(self, position: PaperPosition) -> float:
        return round(position.market_value - position.cost_basis, 2)

    def _return_percent(self, current_price: float, entry_price: float) -> float:
        if entry_price <= 0:
            return 0.0
        return round((current_price - entry_price) / entry_price, 6)

    def _result(
        self,
        position: PaperPosition,
        action: str,
        reason: str,
        unrealized_profit_loss: float,
        unrealized_return_percent: float,
    ) -> PositionMonitorResult:
        return PositionMonitorResult(
            symbol=self._normalize_symbol(position.symbol),
            action=action,
            reason=reason,
            current_price=position.current_price,
            entry_price=position.entry_price,
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )

    def _normalize_symbol(self, symbol: str) -> str:
        return str(symbol).strip().upper()
