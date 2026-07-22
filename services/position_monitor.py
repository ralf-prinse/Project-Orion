from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.risk.time_stop_service import TimeStopService
from services.trading_cost_estimator import TradingCostEstimator


@dataclass(frozen=True)
class PositionMonitorResult:
    symbol: str
    action: str
    reason: str
    current_price: float
    entry_price: float
    unrealized_profit_loss: float
    unrealized_return_percent: float
    estimated_round_trip_costs: float = 0.0
    estimated_net_profit_loss: float = 0.0
    minimum_net_profit: float = 0.0


class PositionMonitor:
    """
    Evaluates whether an open paper position should remain open
    or should be closed.

    Managed-position exit priority:

    1. Dynamic stop loss
    2. Cost-aware net profit/loss threshold when enabled
    3. Final profit target
    4. Maximum holding time
    5. Hold

    This service makes an exit decision, but does not execute it.
    """

    def __init__(
        self,
        time_stop_service: TimeStopService | None = None,
        trading_cost_estimator: TradingCostEstimator | None = None,
    ):
        self.time_stop_service = (
            time_stop_service
            or TimeStopService()
        )
        self.trading_cost_estimator = (
            trading_cost_estimator
            or TradingCostEstimator()
        )

    def evaluate(
        self,
        position: PaperPosition,
        config: LivePaperTradingConfig,
        opened_at: datetime | None = None,
        now: datetime | None = None,
    ) -> PositionMonitorResult:
        unrealized_profit_loss = (
            self._unrealized_profit_loss(position)
        )
        unrealized_return_percent = self._return_percent(
            current_price=position.current_price,
            entry_price=position.entry_price,
        )

        cost_aware_result = self._evaluate_cost_aware_exit(
            position=position,
            config=config,
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )
        if cost_aware_result is not None:
            return cost_aware_result

        if (
            unrealized_return_percent
            >= config.take_profit_percent
        ):
            return self._result(
                position=position,
                action="TAKE_PROFIT",
                reason="Take profit threshold reached.",
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=(
                    unrealized_return_percent
                ),
            )

        if (
            unrealized_return_percent
            <= -config.stop_loss_percent
        ):
            return self._result(
                position=position,
                action="STOP_LOSS",
                reason="Stop loss threshold reached.",
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=(
                    unrealized_return_percent
                ),
            )

        if opened_at is not None:
            temporary_state = PositionState(
                symbol=position.symbol,
                entry_price=position.entry_price,
                current_stop_loss=position.entry_price,
                highest_price=position.current_price,
                current_price=position.current_price,
                opened_at=opened_at,
            )

            time_stop = self.time_stop_service.evaluate(
                state=temporary_state,
                maximum_days=config.max_holding_days,
                now=now,
                maximum_minutes=config.max_holding_minutes,
            )

            if time_stop.activated:
                return self._result(
                    position=position,
                    action="MAX_HOLDING_TIME",
                    reason=time_stop.reason,
                    unrealized_profit_loss=(
                        unrealized_profit_loss
                    ),
                    unrealized_return_percent=(
                        unrealized_return_percent
                    ),
                )

        return self._result(
            position=position,
            action="HOLD",
            reason="No exit condition reached.",
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=(
                unrealized_return_percent
            ),
        )

    def evaluate_managed(
        self,
        position: PaperPosition,
        state: PositionState,
        risk_plan: RiskPlan,
        config: LivePaperTradingConfig | None = None,
        now: datetime | None = None,
    ) -> PositionMonitorResult:
        resolved_config = (
            config
            or LivePaperTradingConfig()
        )

        self._validate_managed_inputs(
            position=position,
            state=state,
            risk_plan=risk_plan,
        )

        unrealized_profit_loss = (
            self._unrealized_profit_loss(position)
        )
        unrealized_return_percent = self._return_percent(
            current_price=position.current_price,
            entry_price=position.entry_price,
        )

        if position.current_price <= state.current_stop_loss:
            return self._result(
                position=position,
                action="STOP_LOSS",
                reason=self._managed_stop_reason(state),
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=(
                    unrealized_return_percent
                ),
            )

        cost_aware_result = self._evaluate_cost_aware_exit(
            position=position,
            config=resolved_config,
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )
        if cost_aware_result is not None:
            return cost_aware_result

        if position.current_price >= risk_plan.target_3:
            return self._result(
                position=position,
                action="TAKE_PROFIT",
                reason="Final profit target reached.",
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=(
                    unrealized_return_percent
                ),
            )

        time_stop = self.time_stop_service.evaluate(
            state=state,
            maximum_days=(
                resolved_config.max_holding_days
            ),
            now=now,
            maximum_minutes=resolved_config.max_holding_minutes,
        )

        if time_stop.activated:
            return self._result(
                position=position,
                action="MAX_HOLDING_TIME",
                reason=time_stop.reason,
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=(
                    unrealized_return_percent
                ),
            )

        return self._result(
            position=position,
            action="HOLD",
            reason="No lifecycle exit condition reached.",
            unrealized_profit_loss=unrealized_profit_loss,
            unrealized_return_percent=(
                unrealized_return_percent
            ),
        )

    def _evaluate_cost_aware_exit(
        self,
        *,
        position: PaperPosition,
        config: LivePaperTradingConfig,
        unrealized_profit_loss: float,
        unrealized_return_percent: float,
    ) -> PositionMonitorResult | None:
        if (
            config.exit_strategy
            != LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT
        ):
            return None

        estimate = self.trading_cost_estimator.estimate_round_trip(
            position=position,
            config=config,
        )
        estimated_net = round(
            unrealized_profit_loss - estimate.total_cost_eur,
            2,
        )
        is_european = position.currency.strip().upper() == "EUR"
        target = (
            config.small_profit_target_eu_eur
            if is_european
            else config.small_profit_target_us_eur
        )
        maximum_loss = (
            config.small_profit_max_loss_eu_eur
            if is_european
            else config.small_profit_max_loss_us_eur
        )

        if estimated_net >= target:
            return self._result(
                position=position,
                action="TAKE_PROFIT",
                reason=(
                    "Cost-aware net profit target reached: "
                    f"estimated net EUR {estimated_net:.2f}, "
                    f"target EUR {target:.2f}, estimated "
                    f"round-trip costs EUR "
                    f"{estimate.total_cost_eur:.2f}."
                ),
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=unrealized_return_percent,
                estimated_round_trip_costs=(
                    estimate.total_cost_eur
                ),
                estimated_net_profit_loss=estimated_net,
                minimum_net_profit=target,
            )

        if estimated_net <= -maximum_loss:
            return self._result(
                position=position,
                action="STOP_LOSS",
                reason=(
                    "Cost-aware net loss limit reached: "
                    f"estimated net EUR {estimated_net:.2f}, "
                    f"limit EUR {-maximum_loss:.2f}, estimated "
                    f"round-trip costs EUR "
                    f"{estimate.total_cost_eur:.2f}."
                ),
                unrealized_profit_loss=unrealized_profit_loss,
                unrealized_return_percent=unrealized_return_percent,
                estimated_round_trip_costs=(
                    estimate.total_cost_eur
                ),
                estimated_net_profit_loss=estimated_net,
                minimum_net_profit=target,
            )

        return None

    def _validate_managed_inputs(
        self,
        position: PaperPosition,
        state: PositionState,
        risk_plan: RiskPlan,
    ) -> None:
        position_symbol = self._normalize_symbol(
            position.symbol
        )

        if not position_symbol:
            raise ValueError(
                "Managed position symbol is required."
            )

        if position_symbol != self._normalize_symbol(
            state.symbol
        ):
            raise ValueError(
                "PositionState symbol does not match "
                "PaperPosition symbol."
            )

        if position_symbol != self._normalize_symbol(
            risk_plan.symbol
        ):
            raise ValueError(
                "RiskPlan symbol does not match "
                "PaperPosition symbol."
            )

        if position.entry_price <= 0:
            raise ValueError(
                "Managed position entry price must "
                "be greater than zero."
            )

        if state.current_stop_loss <= 0:
            raise ValueError(
                "Managed position stop loss must "
                "be greater than zero."
            )

        if risk_plan.target_3 <= 0:
            raise ValueError(
                "Managed position final target must "
                "be greater than zero."
            )

    def _managed_stop_reason(
        self,
        state: PositionState,
    ) -> str:
        if state.trailing_stop_active:
            return "Dynamic trailing stop reached."

        if state.break_even_active:
            return "Break-even stop reached."

        return "Initial lifecycle stop reached."

    def _unrealized_profit_loss(
        self,
        position: PaperPosition,
    ) -> float:
        return round(
            position.market_value
            - position.cost_basis,
            2,
        )

    def _return_percent(
        self,
        current_price: float,
        entry_price: float,
    ) -> float:
        if entry_price <= 0:
            return 0.0

        return round(
            (
                current_price
                - entry_price
            )
            / entry_price,
            6,
        )

    def _result(
        self,
        position: PaperPosition,
        action: str,
        reason: str,
        unrealized_profit_loss: float,
        unrealized_return_percent: float,
        estimated_round_trip_costs: float = 0.0,
        estimated_net_profit_loss: float = 0.0,
        minimum_net_profit: float = 0.0,
    ) -> PositionMonitorResult:
        return PositionMonitorResult(
            symbol=self._normalize_symbol(
                position.symbol
            ),
            action=action,
            reason=reason,
            current_price=position.current_price,
            entry_price=position.entry_price,
            unrealized_profit_loss=(
                unrealized_profit_loss
            ),
            unrealized_return_percent=(
                unrealized_return_percent
            ),
            estimated_round_trip_costs=round(
                estimated_round_trip_costs,
                2,
            ),
            estimated_net_profit_loss=round(
                estimated_net_profit_loss,
                2,
            ),
            minimum_net_profit=round(
                minimum_net_profit,
                2,
            ),
        )

    def _normalize_symbol(
        self,
        symbol: str,
    ) -> str:
        return str(symbol).strip().upper()
