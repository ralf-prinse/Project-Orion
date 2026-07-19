from __future__ import annotations

from models.trade_journal_entry import TradeJournalEntry
from services.dashboard_service import DashboardSnapshot
from ui.foundation.workspace import (
    GuiWorkspace,
    GuiWorkspacePanel,
)


class TradingDashboardGuiPresenter:
    """
    Presenter for the Trading Dashboard GUI.

    Responsibilities:
    - transform DashboardSnapshot into GUI-safe workspace panels
    - transform recent trade journal entries into GUI-safe panels

    Does NOT:
    - calculate statistics
    - load data
    - modify portfolio
    - make trading decisions
    """

    def create_workspace(
        self,
        snapshot: DashboardSnapshot,
        recent_trades: list[TradeJournalEntry] | None = None,
        max_recent_trades: int = 10,
    ) -> GuiWorkspace:
        return GuiWorkspace(
            title="Trading Dashboard",
            subtitle="Live overzicht van paper portfolio, P/L en trading analytics.",
            panels=[
                self._portfolio_panel(snapshot),
                self._trading_panel(snapshot),
                self._closed_trade_analytics_panel(snapshot),
                self._open_positions_panel(snapshot),
                self._risk_decisions_panel(snapshot),
                self._recent_trades_panel(
                    recent_trades=recent_trades or [],
                    max_recent_trades=max_recent_trades,
                ),
            ],
            metadata={},
        )

    def _portfolio_panel(
        self,
        snapshot: DashboardSnapshot,
    ) -> GuiWorkspacePanel:
        return GuiWorkspacePanel(
            panel_type="trading_dashboard_portfolio",
            title="Portfolio",
            subtitle="Cash, equity en totaalresultaat.",
            items=[
                {"label": "Cash", "value": f"€ {snapshot.cash:.2f}"},
                {"label": "Equity", "value": f"€ {snapshot.equity:.2f}"},
                {"label": "Open P/L", "value": f"€ {snapshot.open_profit_loss:.2f}"},
                {"label": "Closed P/L", "value": f"€ {snapshot.closed_profit_loss:.2f}"},
                {"label": "Total P/L", "value": f"€ {snapshot.total_profit_loss:.2f}"},
                {"label": "Return", "value": f"{snapshot.total_return_percent:.2f}%"},
            ],
            status="info",
            metadata={},
        )

    def _risk_decisions_panel(
        self,
        snapshot: DashboardSnapshot,
    ) -> GuiWorkspacePanel:
        items = [
            {
                "label": "Risk Evaluations",
                "value": str(snapshot.risk_evaluations),
            },
            {
                "label": "Risk Rejections",
                "value": str(snapshot.risk_rejections),
            },
        ]

        for decision in reversed(snapshot.risk_decisions[-10:]):
            status = "ALLOWED" if decision.allowed else "BLOCKED"
            metrics = []

            if decision.total_portfolio_risk is not None:
                metrics.append(
                    "portfolio risk "
                    f"{decision.total_portfolio_risk:.4f}"
                )

            if decision.drawdown is not None:
                metrics.append(
                    f"drawdown {decision.drawdown:.4f}"
                )

            metric_text = (
                " | " + ", ".join(metrics)
                if metrics
                else ""
            )
            items.append(
                {
                    "label": decision.symbol,
                    "value": (
                        f"{status}{metric_text} | "
                        f"{decision.reason}"
                    ),
                }
            )

        return GuiWorkspacePanel(
            panel_type="trading_dashboard_risk_decisions",
            title="Risk Decisions",
            subtitle=(
                "Auditbare pre-order risk-gate-uitkomsten uit "
                "het decision journal."
            ),
            items=items,
            status=(
                "warning"
                if snapshot.risk_rejections
                else "neutral"
            ),
            metadata={},
        )

    def _trading_panel(
        self,
        snapshot: DashboardSnapshot,
    ) -> GuiWorkspacePanel:
        return GuiWorkspacePanel(
            panel_type="trading_dashboard_summary",
            title="Trading",
            subtitle="Aantal posities en gesloten trade-statistieken.",
            items=[
                {"label": "Open Positions", "value": str(snapshot.open_positions)},
                {"label": "Closed Trades", "value": str(snapshot.closed_trades)},
                {"label": "Winning Trades", "value": str(snapshot.winning_trades)},
                {"label": "Losing Trades", "value": str(snapshot.losing_trades)},
                {"label": "Winrate", "value": f"{snapshot.winrate_percent:.2f}%"},
            ],
            status="neutral",
            metadata={},
        )

    def _closed_trade_analytics_panel(
        self,
        snapshot: DashboardSnapshot,
    ) -> GuiWorkspacePanel:
        stats = snapshot.closed_trade_statistics

        return GuiWorkspacePanel(
            panel_type="trading_dashboard_closed_analytics",
            title="Closed Trade Analytics",
            subtitle="Deterministische analyse van gesloten trades.",
            items=[
                {"label": "Average Winner", "value": f"€ {stats.average_winner:.2f}"},
                {"label": "Average Loser", "value": f"€ {stats.average_loser:.2f}"},
                {"label": "Profit Factor", "value": f"{stats.profit_factor:.2f}"},
                {"label": "Largest Winner", "value": f"€ {stats.largest_winner:.2f}"},
                {"label": "Largest Loser", "value": f"€ {stats.largest_loser:.2f}"},
            ],
            status="neutral",
            metadata={},
        )

    def _open_positions_panel(
        self,
        snapshot: DashboardSnapshot,
    ) -> GuiWorkspacePanel:
        if not snapshot.positions:
            items = [
                {
                    "label": "Status",
                    "value": "No open positions.",
                }
            ]
        else:
            items = [
                {
                    "label": position.symbol,
                    "value": (
                        f"{position.quantity}x | "
                        f"Entry €{position.entry_price:.2f} | "
                        f"Now €{position.current_price:.2f} | "
                        f"P/L €{position.unrealized_profit_loss:.2f} "
                        f"({position.unrealized_return_percent:.2f}%)"
                    ),
                }
                for position in snapshot.positions
            ]

        return GuiWorkspacePanel(
            panel_type="trading_dashboard_open_positions",
            title="Open Positions",
            subtitle="Actuele paper positions met unrealized P/L.",
            items=items,
            status="neutral",
            metadata={},
        )

    def _recent_trades_panel(
        self,
        recent_trades: list[TradeJournalEntry],
        max_recent_trades: int,
    ) -> GuiWorkspacePanel:
        trade_events = [
            trade
            for trade in recent_trades
            if trade.action in {"OPEN_POSITION", "CLOSE_POSITION"}
        ]

        visible_trades = trade_events[-max_recent_trades:]

        if not visible_trades:
            items = [
                {
                    "label": "Status",
                    "value": "No recent trades.",
                }
            ]
        else:
            items = [
                {
                    "label": trade.symbol,
                    "value": (
                        f"{trade.timestamp:%Y-%m-%d %H:%M:%S} | "
                        f"{trade.action} | "
                        f"{trade.decision} | "
                        f"P/L €{trade.realized_profit_loss:.2f}"
                    ),
                }
                for trade in reversed(visible_trades)
            ]

        return GuiWorkspacePanel(
            panel_type="trading_dashboard_recent_trades",
            title="Recent Trades",
            subtitle="Laatste echte trade-events uit het trade journal.",
            items=items,
            status="neutral",
            metadata={},
        )
