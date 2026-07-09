from __future__ import annotations

from models.trade_journal_entry import TradeJournalEntry
from services.dashboard_service import DashboardSnapshot


class TradingDashboardCliPresenter:
    """
    CLI presenter for the Orion Trading Dashboard.

    Responsibilities:
    - Format DashboardSnapshot for terminal output.
    - Format recent trade journal entries.

    Does NOT:
    - calculate statistics
    - load data
    - modify portfolio
    - make trading decisions
    """

    def present(
        self,
        snapshot: DashboardSnapshot,
        recent_trades: list[TradeJournalEntry] | None = None,
        max_recent_trades: int = 10,
    ) -> str:
        lines: list[str] = []

        lines.append("=" * 60)
        lines.append("ORION TRADING DASHBOARD")
        lines.append("=" * 60)
        lines.append("")

        lines.append("PORTFOLIO")
        lines.append("-" * 60)
        lines.append(f"Cash             : € {snapshot.cash:.2f}")
        lines.append(f"Equity           : € {snapshot.equity:.2f}")
        lines.append(f"Open P/L         : € {snapshot.open_profit_loss:.2f}")
        lines.append(f"Closed P/L       : € {snapshot.closed_profit_loss:.2f}")
        lines.append(f"Total P/L        : € {snapshot.total_profit_loss:.2f}")
        lines.append(f"Return           : {snapshot.total_return_percent:.2f}%")
        lines.append("")

        lines.append("TRADING")
        lines.append("-" * 60)
        lines.append(f"Open Positions   : {snapshot.open_positions}")
        lines.append(f"Closed Trades    : {snapshot.closed_trades}")
        lines.append(f"Winning Trades   : {snapshot.winning_trades}")
        lines.append(f"Losing Trades    : {snapshot.losing_trades}")
        lines.append(f"Winrate          : {snapshot.winrate_percent:.2f}%")
        lines.append("")

        self._append_open_positions(lines, snapshot)
        self._append_recent_trades(
            lines,
            recent_trades or [],
            max_recent_trades,
        )

        return "\n".join(lines)

    def _append_open_positions(
        self,
        lines: list[str],
        snapshot: DashboardSnapshot,
    ) -> None:
        lines.append("OPEN POSITIONS")
        lines.append("-" * 60)

        if not snapshot.positions:
            lines.append("No open positions.")
            lines.append("")
            return

        for position in snapshot.positions:
            lines.append(
                f"{position.symbol:<8}"
                f"{position.quantity:>5}x   "
                f"Entry €{position.entry_price:>8.2f}   "
                f"Now €{position.current_price:>8.2f}   "
                f"P/L €{position.unrealized_profit_loss:>8.2f}"
            )

        lines.append("")

    def _append_recent_trades(
        self,
        lines: list[str],
        recent_trades: list[TradeJournalEntry],
        max_recent_trades: int,
    ) -> None:
        lines.append("RECENT TRADES")
        lines.append("-" * 60)

        trade_events = [
            trade
            for trade in recent_trades
            if trade.action in {"OPEN_POSITION", "CLOSE_POSITION"}
        ]

        if not trade_events:
            lines.append("No recent trades.")
            lines.append("")
            return

        visible_trades = trade_events[-max_recent_trades:]

        for trade in reversed(visible_trades):
            realized = (
                f"€{trade.realized_profit_loss:.2f}"
                if trade.action == "CLOSE_POSITION"
                else "-"
            )

            lines.append(
                f"{trade.timestamp:%Y-%m-%d %H:%M:%S}   "
                f"{trade.symbol:<8}   "
                f"{trade.action:<15}   "
                f"{trade.decision:<15}   "
                f"P/L {realized}"
            )

        lines.append("")