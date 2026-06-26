from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.trade_plan import TradePlan


@dataclass
class ManagedTrade:
    symbol: str
    action: str
    quantity: int
    entry_price: float
    current_price: float
    status: str
    opened_at: str
    max_holding_days: int = 3
    reason: str = ""


class TradeManager:
    """
    TradeManager 1.0

    Beheert de levenscyclus van swing trades:

    SCAN
    -> BUY
    -> HOLD
    -> SELL
    -> LEARN

    In deze eerste versie vertaalt hij TradePlans naar beheerde trades.
    Later wordt dit uitgebreid met:
    - stop loss
    - take profit
    - trailing stop
    - trade history
    - learning engine
    """

    def __init__(self):
        self.open_trades: dict[str, ManagedTrade] = {}

    def process_trade_plans(
        self,
        trade_plans: list[TradePlan],
    ) -> list[ManagedTrade]:
        managed_trades = []

        for plan in trade_plans:
            managed_trade = self.process_trade_plan(plan)

            if managed_trade is not None:
                managed_trades.append(managed_trade)

        return managed_trades

    def process_trade_plan(
        self,
        trade_plan: TradePlan,
    ) -> Optional[ManagedTrade]:
        action = str(trade_plan.action).upper()
        symbol = str(trade_plan.symbol).upper()

        if action == "BUY":
            return self._open_trade(trade_plan)

        if action == "HOLD":
            return self._hold_trade(trade_plan)

        if action == "SELL":
            return self._close_trade(trade_plan)

        return None

    def _open_trade(self, trade_plan: TradePlan) -> ManagedTrade:
        trade = ManagedTrade(
            symbol=trade_plan.symbol,
            action="BUY",
            quantity=trade_plan.quantity,
            entry_price=trade_plan.estimated_price,
            current_price=trade_plan.estimated_price,
            status="OPEN",
            opened_at=datetime.now().isoformat(timespec="seconds"),
            max_holding_days=3,
            reason="Nieuwe swing trade geopend door Orion.",
        )

        self.open_trades[trade.symbol] = trade
        return trade

    def _hold_trade(self, trade_plan: TradePlan) -> ManagedTrade:
        existing_trade = self.open_trades.get(trade_plan.symbol)

        if existing_trade is None:
            return ManagedTrade(
                symbol=trade_plan.symbol,
                action="HOLD",
                quantity=trade_plan.quantity,
                entry_price=trade_plan.estimated_price,
                current_price=trade_plan.estimated_price,
                status="MONITORING",
                opened_at=datetime.now().isoformat(timespec="seconds"),
                max_holding_days=3,
                reason="Orion ziet nog geen reden om te verkopen.",
            )

        existing_trade.action = "HOLD"
        existing_trade.current_price = trade_plan.estimated_price
        existing_trade.status = "MONITORING"
        existing_trade.reason = "Orion blijft deze positie monitoren."

        return existing_trade

    def _close_trade(self, trade_plan: TradePlan) -> ManagedTrade:
        existing_trade = self.open_trades.get(trade_plan.symbol)

        if existing_trade is None:
            return ManagedTrade(
                symbol=trade_plan.symbol,
                action="SELL",
                quantity=trade_plan.quantity,
                entry_price=trade_plan.estimated_price,
                current_price=trade_plan.estimated_price,
                status="CLOSE_SIGNAL",
                opened_at=datetime.now().isoformat(timespec="seconds"),
                max_holding_days=0,
                reason="Orion geeft een verkoopsignaal.",
            )

        existing_trade.action = "SELL"
        existing_trade.current_price = trade_plan.estimated_price
        existing_trade.status = "CLOSE_SIGNAL"
        existing_trade.reason = "Orion adviseert deze positie te sluiten."

        return existing_trade

    def get_open_trades(self) -> list[ManagedTrade]:
        return list(self.open_trades.values())

    def has_open_trade(self, symbol: str) -> bool:
        return symbol.upper() in self.open_trades