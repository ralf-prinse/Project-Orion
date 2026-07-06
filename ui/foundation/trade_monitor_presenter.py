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
            lines.extend(
                [
                    f"{index}. {trade.symbol}",
                    f"   Aantal: {trade.quantity}",
                    f"   Entry: €{trade.entry_price:,.2f}",
                    f"   Huidige koers: €{trade.current_price:,.2f}",
                    f"   Ongerealiseerd P/L: €{trade.unrealized_profit_loss:,.2f} "
                    f"({trade.unrealized_profit_loss_percent:.2f}%)",
                    f"   Stop-loss: €{trade.stop_loss:,.2f}",
                    f"   Take-profit: €{trade.take_profit:,.2f}",
                    f"   Exit status: {trade.exit_signal.value}",
                    "",
                ]
            )

        return TradeMonitorListViewModel(
            title="Open Trades",
            summary=f"{len(trades)} open trade(s) actief.",
            trades_text="\n".join(lines).strip(),
            status="Open trades geladen.",
        )