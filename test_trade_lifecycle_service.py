from __future__ import annotations

from datetime import datetime
from pathlib import Path

from models.trade_lifecycle import ExitSignal, Trade, TradeStatus
from services.open_trade_store import OpenTradeStore
from services.trade_history_store import TradeHistoryStore
from services.trade_lifecycle_service import TradeLifecycleService


OPEN_TEST_FILE = "data/test_open_trades.json"
HISTORY_TEST_FILE = "data/test_trade_history.json"


def cleanup() -> None:
    for filename in (OPEN_TEST_FILE, HISTORY_TEST_FILE):
        path = Path(filename)
        if path.exists():
            path.unlink()


def main():
    cleanup()

    open_store = OpenTradeStore(OPEN_TEST_FILE)
    history_store = TradeHistoryStore(HISTORY_TEST_FILE)

    service = TradeLifecycleService(
        open_trade_store=open_store,
        trade_history_store=history_store,
    )

    print("\n=========================================")
    print("ORION TRADE LIFECYCLE TEST")
    print("=========================================\n")

    trade = Trade(
        symbol="AAPL",
        quantity=2,
        entry_price=300.00,
        entry_datetime=datetime.now(),
        entry_reason="Breakout",
        confidence=95.0,
        current_price=300.00,
        highest_price=300.00,
        lowest_price=300.00,
        stop_loss=285.00,
        take_profit=330.00,
        trailing_stop=None,
        status=TradeStatus.OPEN,
        exit_signal=ExitSignal.HOLD_POSITION,
    )

    service.open_trade(trade)

    trades = service.get_open_trades()

    assert len(trades) == 1

    print("Open trade: PASS")

    service.update_trade_price(
        "AAPL",
        315.00,
    )

    trades = service.get_open_trades()

    updated = trades[0]

    assert updated.current_price == 315.00
    assert updated.highest_price == 315.00
    assert updated.lowest_price == 300.00
    assert updated.unrealized_profit_loss == 30.00

    print("Update trade: PASS")

    service.close_trade(
        "AAPL",
        "Target reached",
    )

    trades = service.get_open_trades()

    assert len(trades) == 0

    history = history_store.load()

    assert len(history) == 1
    assert history[0]["action"] == "SELL"

    print("Close trade: PASS")

    cleanup()

    print("\nTRADE LIFECYCLE: PASS ✅\n")


if __name__ == "__main__":
    main()