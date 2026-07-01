from services.planner.models import TradePlanContext, TradePlannerConfig
from services.planner.trade_planner import TradePlanner


def test_trade_planner_creates_buy_plan_with_calculated_target():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="aapl",
        action="BUY",
        entry_price=100.0,
        stop_loss=95.0,
        recommended_shares=20,
    )

    result = planner.create_plan(context)

    assert result.symbol == "AAPL"
    assert result.action == "BUY"
    assert result.valid_plan is True
    assert result.entry_price == 100.0
    assert result.stop_loss == 95.0
    assert result.target_price == 110.0
    assert result.shares == 20
    assert result.position_value == 2000.0
    assert result.risk_per_share == 5.0
    assert result.total_risk_amount == 100.0
    assert result.expected_reward_amount == 200.0
    assert result.reward_risk_ratio == 2.0


def test_trade_planner_uses_supplied_target_price():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="MSFT",
        action="BUY",
        entry_price=50.0,
        stop_loss=45.0,
        target_price=62.5,
        recommended_shares=10,
    )

    result = planner.create_plan(context)

    assert result.valid_plan is True
    assert result.target_price == 62.5
    assert result.reward_risk_ratio == 2.5


def test_trade_planner_uses_supplied_risk_amount():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="NVDA",
        action="BUY",
        entry_price=100.0,
        stop_loss=90.0,
        recommended_shares=5,
        risk_amount=42.0,
    )

    result = planner.create_plan(context)

    assert result.total_risk_amount == 42.0
    assert result.risk_per_share == 10.0


def test_trade_planner_warns_when_reward_risk_below_minimum():
    planner = TradePlanner()
    config = TradePlannerConfig(minimum_reward_risk_ratio=2.0)
    context = TradePlanContext(
        symbol="TSLA",
        action="BUY",
        entry_price=100.0,
        stop_loss=95.0,
        target_price=107.0,
        recommended_shares=10,
    )

    result = planner.create_plan(context, config)

    assert result.valid_plan is True
    assert result.reward_risk_ratio == 1.4
    assert "Reward/risk ratio is below configured minimum." in result.warnings


def test_trade_planner_rejects_invalid_stop_loss_for_buy():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="AAPL",
        action="BUY",
        entry_price=100.0,
        stop_loss=101.0,
        recommended_shares=10,
    )

    result = planner.create_plan(context)

    assert result.valid_plan is False
    assert result.action == "BUY"
    assert "Stop-loss must be below entry price for BUY plans." in result.warnings


def test_trade_planner_rejects_zero_shares():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="AAPL",
        action="BUY",
        entry_price=100.0,
        stop_loss=95.0,
        recommended_shares=0,
    )

    result = planner.create_plan(context)

    assert result.valid_plan is False
    assert "Recommended shares must be greater than zero." in result.warnings


def test_trade_planner_rejects_unsupported_action():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="AAPL",
        action="WAIT",
        entry_price=100.0,
        stop_loss=95.0,
        recommended_shares=10,
    )

    result = planner.create_plan(context)

    assert result.valid_plan is False
    assert result.action == "NONE"
    assert "Unsupported trade action; no trade plan created." in result.warnings


def test_trade_planner_creates_hold_plan_without_risk_reward():
    planner = TradePlanner()
    context = TradePlanContext(
        symbol="AAPL",
        action="HOLD",
        entry_price=100.0,
        stop_loss=0.0,
        recommended_shares=7,
    )

    result = planner.create_plan(context)

    assert result.valid_plan is True
    assert result.action == "HOLD"
    assert result.shares == 7
    assert result.position_value == 700.0
    assert result.reward_risk_ratio == 0.0
