import json
from datetime import datetime
from pathlib import Path


class TradeHistoryStore:
    def __init__(self, path: str = "data/trade_history.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict]:
        if not self.path.exists():
            self.save([])
            return []

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, trades: list[dict]) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(trades, file, indent=4)

    def add_event(
        self,
        action: str,
        symbol: str,
        quantity: int,
        price: float,
        reason: str = "",
    ) -> None:
        trades = self.load()

        trades.append(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "action": action,
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "reason": reason,
            }
        )

        self.save(trades)