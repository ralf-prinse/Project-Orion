from __future__ import annotations

from datetime import datetime
from pathlib import Path

from models.trade_lifecycle import ExitSignal, Trade, TradeStatus
from services.open_trade_store import OpenTradeStore


TEST_FILE = "data/test_open_trades.json"


def main():
    print("\n=========================================")
    print("ORION OPEN TRADE STORE TEST")
    print("=========================================\n")

    path = Path(TEST_FILE)

    if path.exists():
        path.unlink()

    store = OpenTradeStore(TEST_FILE)

    trade = Trade(
        symbol="AAPL",
        quantity=2,
        entry_price=308.63,
        entry_datetime=datetime.now(),
        entry_reason="Breakout",
        confidence=92.5,
        current_price=308.63,
        highest_price=308.63,
        lowest_price=308.63,
        stop_loss=295.00,
        take_profit=340.00,
        trailing_stop=None,
        status=TradeStatus.OPEN,
        exit_signal=ExitSignal.HOLD_POSITION,
    )

    store.add(trade)

    trades = store.load()

    assert len(trades) == 1
    assert trades[0].symbol == "AAPL"
    assert trades[0].quantity == 2
    assert trades[0].status == TradeStatus.OPEN

    print("Trade opgeslagen: PASS")
    print("Trade geladen: PASS")

    store.remove("AAPL")

    trades = store.load()

    assert len(trades) == 0

    print("Trade verwijderd: PASS")

    if path.exists():
        path.unlink()

    print("\nOPEN TRADE STORE: PASS ✅\n")


if __name__ == "__main__":
    main()