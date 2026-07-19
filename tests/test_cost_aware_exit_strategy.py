from __future__ import annotations

import pytest

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.position_monitor import PositionMonitor
from services.trading_cost_estimator import TradingCostEstimator
from run_autonomous_ibkr_paper import (
    EXIT_STRATEGY_ENVIRONMENT_VARIABLE,
    PRICING_PLAN_ENVIRONMENT_VARIABLE,
    build_config as build_ibkr_config,
    read_exit_strategy,
    read_pricing_plan,
)


def build_state(current_price: float) -> PositionState:
    return PositionState(
        symbol="TEST",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=max(100.0, current_price),
        current_price=current_price,
    )


def build_plan() -> RiskPlan:
    return RiskPlan(
        symbol="TEST",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        target_3=130.0,
        risk_percent=5.0,
        reward_percent=30.0,
        risk_reward_ratio=6.0,
        confidence=0.8,
        notes="Cost-aware exit regression test.",
    )


def build_config(**overrides) -> LivePaperTradingConfig:
    return LivePaperTradingConfig(
        exit_strategy=(
            LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT
        ),
        ibkr_pricing_plan=LivePaperTradingConfig.FIXED_PRICING,
        **overrides,
    )


def evaluate(position: PaperPosition, config=None):
    return PositionMonitor().evaluate_managed(
        position=position,
        state=build_state(position.current_price),
        risk_plan=build_plan(),
        config=config or build_config(),
    )


def test_fixed_us_round_trip_cost_estimate_uses_eur_fx_rate():
    position = PaperPosition(
        symbol="TEST",
        quantity=10,
        entry_price=100.0,
        current_price=101.0,
        currency="USD",
        fx_rate_to_base=0.9,
    )

    result = TradingCostEstimator().estimate_round_trip(
        position=position,
        config=build_config(),
    )

    assert result.buy_commission_eur == 0.9
    assert result.sell_commission_eur == 0.9
    assert result.slippage_eur == 0.9
    assert result.fx_conversion_buffer_eur == 0.54
    assert result.external_fees_eur == 0.25
    assert result.total_cost_eur == 3.5


def test_us_position_exits_only_after_net_eur_target_is_reached():
    hold = evaluate(
        PaperPosition(
            symbol="TEST",
            quantity=10,
            entry_price=100.0,
            current_price=100.8,
            currency="USD",
            fx_rate_to_base=0.9,
        )
    )
    take_profit = evaluate(
        PaperPosition(
            symbol="TEST",
            quantity=10,
            entry_price=100.0,
            current_price=101.0,
            currency="USD",
            fx_rate_to_base=0.9,
        )
    )

    assert hold.action == "HOLD"
    assert take_profit.action == "TAKE_PROFIT"
    assert take_profit.estimated_round_trip_costs == 3.5
    assert take_profit.estimated_net_profit_loss == 5.5
    assert take_profit.minimum_net_profit == 5.0
    assert "estimated net EUR 5.50" in take_profit.reason


def test_us_position_uses_cost_aware_net_loss_limit():
    result = evaluate(
        PaperPosition(
            symbol="TEST",
            quantity=10,
            entry_price=100.0,
            current_price=99.4,
            currency="USD",
            fx_rate_to_base=0.9,
        )
    )

    assert result.action == "STOP_LOSS"
    assert result.estimated_net_profit_loss == -8.89
    assert "net loss limit reached" in result.reason


def test_european_fixed_position_covers_six_euro_commission_floor():
    hold = evaluate(
        PaperPosition(
            symbol="TEST",
            quantity=10,
            entry_price=100.0,
            current_price=101.7,
            currency="EUR",
        )
    )
    take_profit = evaluate(
        PaperPosition(
            symbol="TEST",
            quantity=10,
            entry_price=100.0,
            current_price=101.8,
            currency="EUR",
        )
    )

    assert hold.action == "HOLD"
    assert take_profit.action == "TAKE_PROFIT"
    assert take_profit.estimated_round_trip_costs == 7.26
    assert take_profit.estimated_net_profit_loss == 10.74
    assert take_profit.minimum_net_profit == 10.0


def test_swing_strategy_keeps_existing_final_target_behavior():
    result = evaluate(
        PaperPosition(
            symbol="TEST",
            quantity=10,
            entry_price=100.0,
            current_price=110.0,
            currency="EUR",
        ),
        config=LivePaperTradingConfig(
            exit_strategy=LivePaperTradingConfig.SWING,
        ),
    )

    assert result.action == "HOLD"
    assert result.reason == "No lifecycle exit condition reached."


def test_invalid_cost_strategy_configuration_is_rejected():
    with pytest.raises(ValueError, match="exit_strategy"):
        LivePaperTradingConfig(exit_strategy="UNKNOWN")

    with pytest.raises(ValueError, match="ibkr_pricing_plan"):
        LivePaperTradingConfig(ibkr_pricing_plan="FREE")

    with pytest.raises(
        ValueError,
        match="small_profit_target_us_eur",
    ):
        LivePaperTradingConfig(small_profit_target_us_eur=0.0)


def test_ibkr_runner_defaults_to_cost_aware_fixed_pricing():
    config = build_ibkr_config()

    assert (
        config.live_config.exit_strategy
        == LivePaperTradingConfig.COST_AWARE_SMALL_PROFIT
    )
    assert (
        config.live_config.ibkr_pricing_plan
        == LivePaperTradingConfig.FIXED_PRICING
    )


def test_ibkr_runner_environment_can_select_swing_and_tiered(
    monkeypatch,
):
    monkeypatch.setenv(
        EXIT_STRATEGY_ENVIRONMENT_VARIABLE,
        "swing",
    )
    monkeypatch.setenv(
        PRICING_PLAN_ENVIRONMENT_VARIABLE,
        "tiered",
    )

    assert read_exit_strategy() == LivePaperTradingConfig.SWING
    assert read_pricing_plan() == LivePaperTradingConfig.TIERED_PRICING
