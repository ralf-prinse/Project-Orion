from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition
from services.position_monitor import PositionMonitor


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


def main():
    print("\n=========================================")
    print("ORION POSITION MONITOR TEST")
    print("=========================================\n")

    test_position_monitor_holds_when_no_exit_condition_is_reached()
    test_position_monitor_triggers_take_profit()
    test_position_monitor_triggers_stop_loss()
    test_position_monitor_triggers_max_holding_time()

    print("POSITION MONITOR: PASS ✅")


if __name__ == "__main__":
    main()