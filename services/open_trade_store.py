from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from models.trade_lifecycle import ExitSignal, Trade, TradeStatus


class OpenTradeStore:
    """
    Persistent JSON store for open trades.

    Responsibilities
    ----------------
    - load open trades
    - save open trades
    - add open trade
    - remove open trade

    No UI.
    No trading decisions.
    No exit decisions.
    """

    def __init__(self, path: str = "data/open_trades.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[Trade]:
        if not self.path.exists():
            self.save([])
            return []

        with self.path.open("r", encoding="utf-8") as file:
            raw_trades = json.load(file)

        return [
            self._trade_from_dict(raw_trade)
            for raw_trade in raw_trades
        ]

    def save(self, trades: list[Trade]) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                [
                    self._trade_to_dict(trade)
                    for trade in trades
                ],
                file,
                indent=4,
            )

    def add(self, trade: Trade) -> None:
        trades = self.load()
        trades.append(trade)
        self.save(trades)

    def remove(self, symbol: str) -> None:
        normalized_symbol = str(symbol).strip().upper()

        trades = [
            trade
            for trade in self.load()
            if trade.symbol.upper() != normalized_symbol
        ]

        self.save(trades)

    def _trade_to_dict(self, trade: Trade) -> dict:
        return {
            "symbol": trade.symbol,
            "quantity": trade.quantity,
            "entry_price": trade.entry_price,
            "entry_datetime": trade.entry_datetime.isoformat(timespec="seconds"),
            "entry_reason": trade.entry_reason,
            "confidence": trade.confidence,
            "current_price": trade.current_price,
            "highest_price": trade.highest_price,
            "lowest_price": trade.lowest_price,
            "stop_loss": trade.stop_loss,
            "take_profit": trade.take_profit,
            "trailing_stop": trade.trailing_stop,
            "status": trade.status.value,
            "exit_signal": trade.exit_signal.value,
            "exit_reason": trade.exit_reason,
            "exit_price": trade.exit_price,
            "exit_datetime": (
                trade.exit_datetime.isoformat(timespec="seconds")
                if trade.exit_datetime is not None
                else None
            ),
            "realized_profit_loss": trade.realized_profit_loss,
            "unrealized_profit_loss": trade.unrealized_profit_loss,
            "unrealized_profit_loss_percent": trade.unrealized_profit_loss_percent,
            "notes": trade.notes,
        }

    def _trade_from_dict(self, data: dict) -> Trade:
        return Trade(
            symbol=str(data.get("symbol", "")).upper(),
            quantity=int(data.get("quantity", 0)),
            entry_price=float(data.get("entry_price", 0.0)),
            entry_datetime=datetime.fromisoformat(
                data.get("entry_datetime")
            ),
            entry_reason=str(data.get("entry_reason", "")),
            confidence=float(data.get("confidence", 0.0)),
            current_price=float(data.get("current_price", 0.0)),
            highest_price=float(data.get("highest_price", 0.0)),
            lowest_price=float(data.get("lowest_price", 0.0)),
            stop_loss=float(data.get("stop_loss", 0.0)),
            take_profit=float(data.get("take_profit", 0.0)),
            trailing_stop=(
                float(data["trailing_stop"])
                if data.get("trailing_stop") is not None
                else None
            ),
            status=TradeStatus(data.get("status", TradeStatus.OPEN.value)),
            exit_signal=ExitSignal(
                data.get("exit_signal", ExitSignal.HOLD_POSITION.value)
            ),
            exit_reason=str(data.get("exit_reason", "")),
            exit_price=(
                float(data["exit_price"])
                if data.get("exit_price") is not None
                else None
            ),
            exit_datetime=(
                datetime.fromisoformat(data["exit_datetime"])
                if data.get("exit_datetime") is not None
                else None
            ),
            realized_profit_loss=float(data.get("realized_profit_loss", 0.0)),
            unrealized_profit_loss=float(data.get("unrealized_profit_loss", 0.0)),
            unrealized_profit_loss_percent=float(
                data.get("unrealized_profit_loss_percent", 0.0)
            ),
            notes=str(data.get("notes", "")),
        )