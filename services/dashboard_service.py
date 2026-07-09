from __future__ import annotations

from dataclasses import dataclass

from models.paper_portfolio import PaperPortfolio
from models.trade_journal_entry import TradeJournalEntry


@dataclass(frozen=True)
class DashboardPosition:
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    market_value: float
    unrealized_profit_loss: float
    unrealized_return_percent: float


@dataclass(frozen=True)
class DashboardSnapshot:
    cash: float
    equity: float
    open_positions: int
    open_profit_loss: float
    closed_profit_loss: float
    total_profit_loss: float
    total_return_percent: float
    closed_trades: int
    winning_trades: int
    losing_trades: int
    winrate_percent: float
    positions: list[DashboardPosition]


class DashboardService:
    def build(
        self,
        portfolio: PaperPortfolio,
        journal_entries: list[TradeJournalEntry],
        initial_cash: float,
    ) -> DashboardSnapshot:
        positions = [
            self._build_position(symbol, position)
            for symbol, position in portfolio.positions.items()
        ]

        open_profit_loss = round(
            sum(position.unrealized_profit_loss for position in positions),
            2,
        )

        closed_entries = [
            entry
            for entry in journal_entries
            if entry.action == "CLOSE_POSITION"
        ]

        closed_profit_loss = round(
            sum(entry.realized_profit_loss for entry in closed_entries),
            2,
        )

        winning_trades = len(
            [
                entry
                for entry in closed_entries
                if entry.realized_profit_loss > 0
            ]
        )

        losing_trades = len(
            [
                entry
                for entry in closed_entries
                if entry.realized_profit_loss < 0
            ]
        )

        closed_trades = len(closed_entries)

        winrate_percent = (
            round((winning_trades / closed_trades) * 100, 2)
            if closed_trades > 0
            else 0.0
        )

        total_profit_loss = round(
            open_profit_loss + closed_profit_loss,
            2,
        )

        total_return_percent = (
            round((total_profit_loss / initial_cash) * 100, 2)
            if initial_cash > 0
            else 0.0
        )

        return DashboardSnapshot(
            cash=round(portfolio.cash, 2),
            equity=portfolio.equity,
            open_positions=len(portfolio.positions),
            open_profit_loss=open_profit_loss,
            closed_profit_loss=closed_profit_loss,
            total_profit_loss=total_profit_loss,
            total_return_percent=total_return_percent,
            closed_trades=closed_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            winrate_percent=winrate_percent,
            positions=positions,
        )

    def _build_position(
        self,
        symbol,
        position,
    ) -> DashboardPosition:
        unrealized_return_percent = (
            round(
                (
                    (position.current_price - position.entry_price)
                    / position.entry_price
                )
                * 100,
                2,
            )
            if position.entry_price > 0
            else 0.0
        )

        return DashboardPosition(
            symbol=symbol,
            quantity=position.quantity,
            entry_price=position.entry_price,
            current_price=position.current_price,
            market_value=position.market_value,
            unrealized_profit_loss=position.unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )