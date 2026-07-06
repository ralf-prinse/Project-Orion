from __future__ import annotations

from datetime import datetime
from pathlib import Path

from models.trade_lifecycle import ExitSignal, Trade, TradeStatus
from services.open_trade_store import OpenTradeStore
from services.trade_history_store import TradeHistoryStore
from services.trade_lifecycle_service import TradeLifecycleService
from services.trade_monitor_service import TradeMonitorService


OPEN_TEST_FILE = "data/test_monitor_open_trades.json"
HISTORY_TEST_FILE = "data/test_monitor_trade_history.json"


def cleanup() -> None:
    for filename in (OPEN_TEST_FILE, HISTORY_TEST_FILE):
        path = Path(filename)
        if path.exists():
            path.unlink()


def create_trade(
    current_price: float = 300.0,
    stop_loss: float = 285.0,
    take_profit: float = 330.0,
) -> Trade:
    return Trade(
        symbol="AAPL",
        quantity=1,
        entry_price=300.0,
        entry_datetime=datetime.now(),
        entry_reason="Breakout",
        confidence=90.0,
        current_price=current_price,
        highest_price=current_price,
        lowest_price=current_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
        trailing_stop=None,
        status=TradeStatus.OPEN,
        exit_signal=ExitSignal.HOLD_POSITION,
    )


def main():
    cleanup()

    lifecycle = TradeLifecycleService(
        open_trade_store=OpenTradeStore(OPEN_TEST_FILE),
        trade_history_store=TradeHistoryStore(HISTORY_TEST_FILE),
    )

    monitor = TradeMonitorService(lifecycle)

    print("\n=========================================")
    print("ORION TRADE MONITOR TEST")
    print("=========================================\n")

    trade = create_trade()
    lifecycle.open_trade(trade)

    trades = monitor.get_open_trades()
    assert len(trades) == 1
    print("Open trades ophalen: PASS")

    monitor.update_trade(
        symbol="AAPL",
        current_price=315.0,
    )

    updated = monitor.get_open_trades()[0]

    assert updated.current_price == 315.0
    assert updated.highest_price == 315.0
    assert updated.unrealized_profit_loss == 15.0

    print("Trade monitor update: PASS")

    evaluated_hold = monitor.evaluate_trade(updated)

    assert evaluated_hold.exit_signal == ExitSignal.HOLD_POSITION
    assert evaluated_hold.exit_reason

    print("Exit evaluation HOLD: PASS")

    stop_loss_trade = create_trade(
        current_price=280.0,
        stop_loss=285.0,
        take_profit=330.0,
    )

    evaluated_stop = monitor.evaluate_trade(stop_loss_trade)

    assert evaluated_stop.exit_signal == ExitSignal.STOP_LOSS
    assert evaluated_stop.exit_reason

    print("Exit evaluation STOP LOSS: PASS")

    take_profit_trade = create_trade(
        current_price=335.0,
        stop_loss=285.0,
        take_profit=330.0,
    )

    evaluated_target = monitor.evaluate_trade(take_profit_trade)

    assert evaluated_target.exit_signal == ExitSignal.TAKE_PROFIT
    assert evaluated_target.exit_reason

    print("Exit evaluation TAKE PROFIT: PASS")

    refreshed = monitor.refresh_all()

    assert refreshed == 1

    print("Refresh loop: PASS")

    cleanup()

    print("\nTRADE MONITOR SERVICE: PASS ✅\n")


if __name__ == "__main__":
    main()