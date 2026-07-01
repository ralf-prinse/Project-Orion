from services.performance.models import PerformanceResult
from ui.foundation.models import GuiMetric, GuiSection


class PerformanceDashboardPresenter:
    """
    Builds dashboard-ready performance sections for the GUI.

    This presenter is intentionally display-only. It consumes a completed
    PerformanceResult from the deterministic Performance Analytics layer and
    turns it into stable GUI sections. It never calculates performance metrics,
    never changes portfolio state and never makes trading decisions.
    """

    def create_sections(self, result: PerformanceResult) -> list[GuiSection]:
        sections = [
            self._create_summary_section(result),
            self._create_trade_quality_section(result),
            self._create_risk_section(result),
        ]

        diagnostics = self._create_diagnostics_section(result)
        if diagnostics is not None:
            sections.append(diagnostics)

        return sections

    def _create_summary_section(self, result: PerformanceResult) -> GuiSection:
        return GuiSection(
            title="Performance Dashboard",
            description="High-level performance summary from deterministic analytics.",
            metrics=[
                GuiMetric("Label", result.label or "Performance"),
                GuiMetric("Valid Analysis", "Yes" if result.valid_analysis else "No"),
                GuiMetric("Net P/L", f"{result.net_pnl:.2f}"),
                GuiMetric("Total Return", f"{result.total_return_pct:.2f}%"),
                GuiMetric("Ending Equity", f"{result.ending_equity:.2f}"),
            ],
        )

    def _create_trade_quality_section(self, result: PerformanceResult) -> GuiSection:
        return GuiSection(
            title="Trade Quality",
            description="Trade distribution and expectancy metrics.",
            metrics=[
                GuiMetric("Total Trades", str(result.total_trades)),
                GuiMetric("Winning Trades", str(result.winning_trades)),
                GuiMetric("Losing Trades", str(result.losing_trades)),
                GuiMetric("Breakeven Trades", str(result.breakeven_trades)),
                GuiMetric("Win Rate", f"{result.win_rate:.2f}%"),
                GuiMetric("Expectancy", f"{result.expectancy:.2f}"),
            ],
        )

    def _create_risk_section(self, result: PerformanceResult) -> GuiSection:
        return GuiSection(
            title="Risk & Drawdown",
            description="Capital protection metrics calculated by Performance Analytics.",
            metrics=[
                GuiMetric("Starting Equity", f"{result.starting_equity:.2f}"),
                GuiMetric("Max Drawdown", f"{result.max_drawdown_pct:.2f}%"),
                GuiMetric("Max Drawdown Amount", f"{result.max_drawdown_amount:.2f}"),
                GuiMetric("Profit Factor", f"{result.profit_factor:.2f}"),
                GuiMetric("Payoff Ratio", f"{result.payoff_ratio:.2f}"),
            ],
        )

    def _create_diagnostics_section(self, result: PerformanceResult) -> GuiSection | None:
        diagnostics: list[GuiMetric] = []

        for index, warning in enumerate(result.warnings, start=1):
            diagnostics.append(GuiMetric(f"Warning {index}", warning))

        for index, reason in enumerate(result.reasons, start=1):
            diagnostics.append(GuiMetric(f"Reason {index}", reason))

        if not diagnostics:
            return None

        return GuiSection(
            title="Performance Diagnostics",
            description="Deterministic warnings and reasons from the analytics layer.",
            metrics=diagnostics,
        )
