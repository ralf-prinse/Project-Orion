from services.performance.models import PerformanceResult
from ui.foundation.models import GuiMetric, GuiSection


class DashboardPresenter:
    """
    Converts deterministic engine outputs into dashboard sections.

    This presenter formats existing results only. It never calculates signals,
    decisions, position sizing, portfolio constraints, risk acceptance or trade
    plans.
    """

    def create_overview_sections(
        self,
        performance_result: PerformanceResult | None = None,
        total_open_positions: int = 0,
        total_watchlist_items: int = 0,
    ) -> list[GuiSection]:
        sections = [
            GuiSection(
                title="System Overview",
                description="High-level deterministic platform status.",
                metrics=[
                    GuiMetric("Open Positions", str(total_open_positions)),
                    GuiMetric("Watchlist Items", str(total_watchlist_items)),
                ],
            )
        ]

        if performance_result is not None:
            sections.append(
                GuiSection(
                    title="Performance Snapshot",
                    description="Summary generated from Performance Analytics.",
                    metrics=[
                        GuiMetric("Trades", str(performance_result.total_trades)),
                        GuiMetric("Win Rate", f"{performance_result.win_rate:.2f}%"),
                        GuiMetric("Net P/L", f"{performance_result.net_pnl:.2f}"),
                        GuiMetric("Max Drawdown", f"{performance_result.max_drawdown_pct:.2f}%"),
                    ],
                )
            )

        return sections
