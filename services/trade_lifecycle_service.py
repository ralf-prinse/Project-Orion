from __future__ import annotations

from dataclasses import replace

from models.trade_lifecycle import Trade
from services.open_trade_store import OpenTradeStore
from services.trade_history_store import TradeHistoryStore


class TradeLifecycleService:
    """
    Coordinates the lifecycle of open trades.

    Responsibilities
    ----------------
    - Open a trade
    - Update an open trade
    - Close a trade
    - Move closed trades to history

    Does NOT:
    - Generate BUY/HOLD/SELL signals
    - Generate HOLD/EXIT decisions
    """

    def __init__(
        self,
        open_trade_store: OpenTradeStore | None = None,
        trade_history_store: TradeHistoryStore | None = None,
    ) -> None:
        self._open_trade_store = open_trade_store or OpenTradeStore()
        self._history_store = trade_history_store or TradeHistoryStore()

    def get_open_trades(self) -> list[Trade]:
        return self._open_trade_store.load()

    def open_trade(self, trade: Trade) -> None:
        self._open_trade_store.add(trade)

    def update_trade_price(
        self,
        symbol: str,
        current_price: float,
    ) -> None:
        trades = self._open_trade_store.load()

        updated: list[Trade] = []

        for trade in trades:
            if trade.symbol.upper() != symbol.upper():
                updated.append(trade)
                continue

            highest = max(trade.highest_price, current_price)
            lowest = min(trade.lowest_price, current_price)

            pnl = (current_price - trade.entry_price) * trade.quantity

            pnl_pct = (
                ((current_price - trade.entry_price) / trade.entry_price) * 100
                if trade.entry_price > 0
                else 0.0
            )

            updated.append(
                replace(
                    trade,
                    current_price=current_price,
                    highest_price=highest,
                    lowest_price=lowest,
                    unrealized_profit_loss=round(pnl, 2),
                    unrealized_profit_loss_percent=round(pnl_pct, 2),
                )
            )

        self._open_trade_store.save(updated)

    def close_trade(
        self,
        symbol: str,
        reason: str,
    ) -> None:
        trades = self._open_trade_store.load()

        remaining: list[Trade] = []

        for trade in trades:
            if trade.symbol.upper() != symbol.upper():
                remaining.append(trade)
                continue

            self._history_store.add_event(
                action="SELL",
                symbol=trade.symbol,
                quantity=trade.quantity,
                price=trade.current_price,
                reason=reason,
            )

        self._open_trade_store.save(remaining)