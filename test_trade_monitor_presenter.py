from __future__ import annotations

from datetime import datetime

from models.trade_lifecycle import ExitSignal, Trade, TradeStatus
from ui.foundation.trade_monitor_presenter import TradeMonitorPresenter


def main():
    presenter = TradeMonitorPresenter()

    print("\n=========================================")
    print("ORION TRADE MONITOR PRESENTER TEST")
    print("=========================================\n")

    empty = presenter.present_open_trades([])

    assert empty.title == "Open Trades"
    assert "Geen open trades" in empty.summary

    print("Lege lijst: PASS")

    trade = Trade(
        symbol="AAPL",
        quantity=2,
        entry_price=300.0,
        entry_datetime=datetime.now(),
        entry_reason="Breakout",
        confidence=95.0,
        current_price=315.0,
        highest_price=320.0,
        lowest_price=299.0,
        stop_loss=285.0,
        take_profit=340.0,
        trailing_stop=None,
        status=TradeStatus.OPEN,
        exit_signal=ExitSignal.HOLD_POSITION,
        unrealized_profit_loss=30.0,
        unrealized_profit_loss_percent=5.0,
    )

    result = presenter.present_open_trades([trade])

    assert result.title == "Open Trades"
    assert "1 open trade" in result.summary
    assert "AAPL" in result.trades_text
    assert "Aantal:" in result.trades_text
    assert "2" in result.trades_text
    assert "Exit status: HOLD_POSITION" in result.trades_text

    print("Open trade formatter: PASS")

    print("\nTRADE MONITOR PRESENTER: PASS ✅\n")


if __name__ == "__main__":
    main()