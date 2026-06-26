from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.portfolio import Portfolio
from models.trade_plan import TradePlan
from services.portfolio_store import PortfolioStore
from services.trade_history_store import TradeHistoryStore


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
    def __init__(
        self,
        portfolio_store: PortfolioStore | None = None,
        trade_history_store: TradeHistoryStore | None = None,
    ):
        self.open_trades: dict[str, ManagedTrade] = {}
        self.portfolio_store = portfolio_store or PortfolioStore()
        self.trade_history_store = trade_history_store or TradeHistoryStore()

    def process_trade_plans(
        self,
        trade_plans: list[TradePlan],
        portfolio: Portfolio,
        execute: bool = True,
    ) -> list[ManagedTrade]:
        managed_trades = []

        for plan in trade_plans:
            managed_trade = self.process_trade_plan(
                trade_plan=plan,
                portfolio=portfolio,
                execute=execute,
            )

            if managed_trade is not None:
                managed_trades.append(managed_trade)

        if execute:
            self.portfolio_store.save(portfolio)

        return managed_trades

    def process_trade_plan(
        self,
        trade_plan: TradePlan,
        portfolio: Portfolio,
        execute: bool = True,
    ) -> Optional[ManagedTrade]:
        action = str(trade_plan.action).upper()

        if action == "BUY":
            return self._open_trade(
                trade_plan=trade_plan,
                portfolio=portfolio,
                execute=execute,
            )

        if action == "HOLD":
            return self._hold_trade(trade_plan)

        if action == "SELL":
            return self._close_trade(
                trade_plan=trade_plan,
                portfolio=portfolio,
                execute=execute,
            )

        return None

    def _open_trade(
        self,
        trade_plan: TradePlan,
        portfolio: Portfolio,
        execute: bool,
    ) -> ManagedTrade:
        trade = ManagedTrade(
            symbol=trade_plan.symbol,
            action="BUY",
            quantity=trade_plan.quantity,
            entry_price=trade_plan.estimated_price,
            current_price=trade_plan.estimated_price,
            status="OPEN",
            opened_at=datetime.now().isoformat(timespec="seconds"),
            max_holding_days=3,
            reason="Orion adviseert deze swing trade te openen.",
        )

        self.open_trades[trade.symbol] = trade

        if execute and trade.quantity > 0:
            portfolio.buy(
                symbol=trade.symbol,
                quantity=trade.quantity,
                price=trade.entry_price,
            )

            self.trade_history_store.add_event(
                action="BUY",
                symbol=trade.symbol,
                quantity=trade.quantity,
                price=trade.entry_price,
                reason=trade.reason,
            )

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

    def _close_trade(
        self,
        trade_plan: TradePlan,
        portfolio: Portfolio,
        execute: bool,
    ) -> ManagedTrade:
        existing_trade = self.open_trades.get(trade_plan.symbol)

        quantity = trade_plan.quantity

        if quantity <= 0:
            quantity = portfolio.get_position_quantity(trade_plan.symbol)

        if existing_trade is None:
            trade = ManagedTrade(
                symbol=trade_plan.symbol,
                action="SELL",
                quantity=quantity,
                entry_price=trade_plan.estimated_price,
                current_price=trade_plan.estimated_price,
                status="CLOSE_SIGNAL",
                opened_at=datetime.now().isoformat(timespec="seconds"),
                max_holding_days=0,
                reason="Orion geeft een verkoopsignaal.",
            )
        else:
            existing_trade.action = "SELL"
            existing_trade.quantity = quantity
            existing_trade.current_price = trade_plan.estimated_price
            existing_trade.status = "CLOSE_SIGNAL"
            existing_trade.reason = "Orion adviseert deze positie te sluiten."
            trade = existing_trade

        if execute and quantity > 0:
            portfolio.sell(
                symbol=trade.symbol,
                quantity=quantity,
                price=trade.current_price,
            )

            self.trade_history_store.add_event(
                action="SELL",
                symbol=trade.symbol,
                quantity=quantity,
                price=trade.current_price,
                reason=trade.reason,
            )

            self.open_trades.pop(trade.symbol, None)

        return trade

    def get_open_trades(self) -> list[ManagedTrade]:
        return list(self.open_trades.values())

    def has_open_trade(self, symbol: str) -> bool:
        return symbol.upper() in self.open_trades