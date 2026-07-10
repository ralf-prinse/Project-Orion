from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.risk_plan import RiskPlan
from services.position_monitor import PositionMonitor


def build_position(
    current_price: float,
) -> PaperPosition:
    return PaperPosition(
        symbol="TEST",
        quantity=1,
        entry_price=100.0,
        current_price=current_price,
    )


def build_position_state(
    current_price: float,
    current_stop_loss: float = 95.0,
    highest_price: float = 100.0,
    break_even_active: bool = False,
    trailing_stop_active: bool = False,
    target_1_hit: bool = False,
    target_2_hit: bool = False,
    target_3_hit: bool = False,
) -> PositionState:
    return PositionState(
        symbol="TEST",
        entry_price=100.0,
        current_stop_loss=current_stop_loss,
        highest_price=highest_price,
        current_price=current_price,
        break_even_active=break_even_active,
        trailing_stop_active=trailing_stop_active,
        target_1_hit=target_1_hit,
        target_2_hit=target_2_hit,
        target_3_hit=target_3_hit,
    )


def build_risk_plan() -> RiskPlan:
    return RiskPlan(
        symbol="TEST",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=110.0,
        target_2=120.0,
        target_3=130.0,
        risk_percent=0.05,
        reward_percent=0.30,
        risk_reward_ratio=6.0,
        confidence=0.80,
        notes="Position monitor regression test.",
    )


def test_position_monitor_holds_when_no_exit_condition_is_reached():
    monitor = PositionMonitor()
    config = LivePaperTradingConfig(
        take_profit_percent=0.08,
        stop_loss_percent=0.04,
    )

    position = PaperPosition(
        symbol="TEST",
        quantity=1,
        entry_price=100.0,
        current_price=102.0,
    )

    result = monitor.evaluate(
        position=position,
        config=config,
    )

    assert result.symbol == "TEST"
    assert result.action == "HOLD"
    assert result.reason == "No exit condition reached."
    assert result.unrealized_profit_loss == 2.0
    assert result.unrealized_return_percent == 0.02


def test_position_monitor_triggers_take_profit():
    monitor = PositionMonitor()
    config = LivePaperTradingConfig(
        take_profit_percent=0.08,
        stop_loss_percent=0.04,
    )

    position = PaperPosition(
        symbol="TEST",
        quantity=2,
        entry_price=100.0,
        current_price=108.0,
    )

    result = monitor.evaluate(
        position=position,
        config=config,
    )

    assert result.action == "TAKE_PROFIT"
    assert result.reason == "Take profit threshold reached."
    assert result.unrealized_profit_loss == 16.0
    assert result.unrealized_return_percent == 0.08


def test_position_monitor_triggers_stop_loss():
    monitor = PositionMonitor()
    config = LivePaperTradingConfig(
        take_profit_percent=0.08,
        stop_loss_percent=0.04,
    )

    position = PaperPosition(
        symbol="TEST",
        quantity=1,
        entry_price=100.0,
        current_price=96.0,
    )

    result = monitor.evaluate(
        position=position,
        config=config,
    )

    assert result.action == "STOP_LOSS"
    assert result.reason == "Stop loss threshold reached."
    assert result.unrealized_profit_loss == -4.0
    assert result.unrealized_return_percent == -0.04


def test_position_monitor_triggers_max_holding_time():
    monitor = PositionMonitor()
    config = LivePaperTradingConfig(
        max_holding_days=20,
    )

    position = PaperPosition(
        symbol="TEST",
        quantity=1,
        entry_price=100.0,
        current_price=101.0,
    )

    opened_at = datetime(2026, 1, 1)
    now = opened_at + timedelta(days=20)

    result = monitor.evaluate(
        position=position,
        config=config,
        opened_at=opened_at,
        now=now,
    )

    assert result.action == "MAX_HOLDING_TIME"
    assert result.reason == "Maximum holding period reached."


def test_managed_position_holds_when_no_lifecycle_exit_is_reached():
    monitor = PositionMonitor()
    position = build_position(current_price=105.0)
    state = build_position_state(
        current_price=105.0,
        current_stop_loss=95.0,
        highest_price=105.0,
    )
    risk_plan = build_risk_plan()

    result = monitor.evaluate_managed(
        position=position,
        state=state,
        risk_plan=risk_plan,
    )

    assert result.symbol == "TEST"
    assert result.action == "HOLD"
    assert result.reason == "No lifecycle exit condition reached."
    assert result.unrealized_profit_loss == 5.0
    assert result.unrealized_return_percent == 0.05


def test_managed_position_triggers_initial_stop_loss():
    monitor = PositionMonitor()
    position = build_position(current_price=94.0)
    state = build_position_state(
        current_price=94.0,
        current_stop_loss=95.0,
        highest_price=100.0,
    )
    risk_plan = build_risk_plan()

    result = monitor.evaluate_managed(
        position=position,
        state=state,
        risk_plan=risk_plan,
    )

    assert result.action == "STOP_LOSS"
    assert result.reason == "Initial lifecycle stop reached."
    assert result.current_price == 94.0
    assert result.unrealized_profit_loss == -6.0


def test_managed_position_triggers_break_even_stop():
    monitor = PositionMonitor()
    position = build_position(current_price=99.0)
    state = build_position_state(
        current_price=99.0,
        current_stop_loss=100.0,
        highest_price=111.0,
        break_even_active=True,
    )
    risk_plan = build_risk_plan()

    result = monitor.evaluate_managed(
        position=position,
        state=state,
        risk_plan=risk_plan,
    )

    assert result.action == "STOP_LOSS"
    assert result.reason == "Break-even stop reached."
    assert result.current_price == 99.0
    assert result.unrealized_profit_loss == -1.0


def test_managed_position_triggers_trailing_stop():
    monitor = PositionMonitor()
    position = build_position(current_price=113.0)
    state = build_position_state(
        current_price=113.0,
        current_stop_loss=114.0,
        highest_price=120.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=True,
    )
    risk_plan = build_risk_plan()

    result = monitor.evaluate_managed(
        position=position,
        state=state,
        risk_plan=risk_plan,
    )

    assert result.action == "STOP_LOSS"
    assert result.reason == "Dynamic trailing stop reached."
    assert result.current_price == 113.0
    assert result.unrealized_profit_loss == 13.0


def test_managed_position_triggers_final_profit_target():
    monitor = PositionMonitor()
    position = build_position(current_price=130.0)
    state = build_position_state(
        current_price=130.0,
        current_stop_loss=114.0,
        highest_price=130.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=True,
        target_3_hit=True,
    )
    risk_plan = build_risk_plan()

    result = monitor.evaluate_managed(
        position=position,
        state=state,
        risk_plan=risk_plan,
    )

    assert result.action == "TAKE_PROFIT"
    assert result.reason == "Final profit target reached."
    assert result.current_price == 130.0
    assert result.unrealized_profit_loss == 30.0
    assert result.unrealized_return_percent == 0.30


def test_managed_position_does_not_exit_at_target_1_or_target_2():
    monitor = PositionMonitor()
    risk_plan = build_risk_plan()

    target_1_position = build_position(current_price=111.0)
    target_1_state = build_position_state(
        current_price=111.0,
        current_stop_loss=100.0,
        highest_price=111.0,
        break_even_active=True,
        target_1_hit=True,
    )

    target_1_result = monitor.evaluate_managed(
        position=target_1_position,
        state=target_1_state,
        risk_plan=risk_plan,
    )

    assert target_1_result.action == "HOLD"

    target_2_position = build_position(current_price=121.0)
    target_2_state = build_position_state(
        current_price=121.0,
        current_stop_loss=114.95,
        highest_price=121.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=True,
    )

    target_2_result = monitor.evaluate_managed(
        position=target_2_position,
        state=target_2_state,
        risk_plan=risk_plan,
    )

    assert target_2_result.action == "HOLD"


def main():
    print("\n=========================================")
    print("ORION POSITION MONITOR TEST")
    print("=========================================\n")

    test_position_monitor_holds_when_no_exit_condition_is_reached()
    test_position_monitor_triggers_take_profit()
    test_position_monitor_triggers_stop_loss()
    test_position_monitor_triggers_max_holding_time()
    test_managed_position_holds_when_no_lifecycle_exit_is_reached()
    test_managed_position_triggers_initial_stop_loss()
    test_managed_position_triggers_break_even_stop()
    test_managed_position_triggers_trailing_stop()
    test_managed_position_triggers_final_profit_target()
    test_managed_position_does_not_exit_at_target_1_or_target_2()

    print("POSITION MONITOR: PASS ✅")


if __name__ == "__main__":
    main()