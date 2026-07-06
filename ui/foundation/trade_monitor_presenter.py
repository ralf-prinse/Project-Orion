from __future__ import annotations

from dataclasses import dataclass

from models.trade_lifecycle import Trade


@dataclass(frozen=True)
class TradeMonitorListViewModel:
    title: str
    summary: str
    trades_text: str
    status: str


class TradeMonitorPresenter:
    """
    Presentation-only formatter for Trade Monitor overview.

    Responsibilities
    ----------------
    - format open trades for GUI display
    - create readable summaries
    - format visual trade status indicators

    No business logic.
    No persistence.
    No exit decisions.
    """

    def present_open_trades(
        self,
        trades: list[Trade],
    ) -> TradeMonitorListViewModel:
        if not trades:
            return TradeMonitorListViewModel(
                title="Open Trades",
                summary="Geen open trades gevonden.",
                trades_text="Er zijn momenteel geen open trades opgeslagen.",
                status="Trade Monitor geladen.",
            )

        lines: list[str] = []

        for index, trade in enumerate(trades, start=1):
            lines.extend(self._format_trade(index, trade))

        return TradeMonitorListViewModel(
            title="Open Trades",
            summary=f"{len(trades)} open trade(s) actief.",
            trades_text="\n".join(lines).strip(),
            status="Open trades geladen.",
        )

    def _format_trade(
        self,
        index: int,
        trade: Trade,
    ) -> list[str]:
        price_icon = self._price_direction_icon(trade)
        pnl_icon = self._pnl_icon(trade)
        exit_icon = self._exit_icon(trade)

        return [
            f"{index}. {trade.symbol}",
            f"   Aantal: {trade.quantity}",
            f"   Entry: €{trade.entry_price:,.2f}",
            (
                f"   {price_icon} Huidige koers: "
                f"€{trade.current_price:,.2f}"
            ),
            (
                f"   {pnl_icon} Ongerealiseerd P/L: "
                f"€{trade.unrealized_profit_loss:,.2f} "
                f"({trade.unrealized_profit_loss_percent:.2f}%)"
            ),
            f"   Stop-loss: €{trade.stop_loss:,.2f}",
            f"   Take-profit: €{trade.take_profit:,.2f}",
            f"   {exit_icon} Exit status: {trade.exit_signal.value}",
            "",
        ]

    def _price_direction_icon(self, trade: Trade) -> str:
        if trade.current_price > trade.entry_price:
            return "🟢"

        if trade.current_price < trade.entry_price:
            return "🔴"

        return "⚪"

    def _pnl_icon(self, trade: Trade) -> str:
        if trade.unrealized_profit_loss > 0:
            return "🟢"

        if trade.unrealized_profit_loss < 0:
            return "🔴"

        return "⚪"

    def _exit_icon(self, trade: Trade) -> str:
        value = str(trade.exit_signal.value).upper()

        if value == "HOLD_POSITION":
            return "🟢"

        if value in {"TAKE_PROFIT", "TRAILING_STOP"}:
            return "🟡"

        return "🔴"