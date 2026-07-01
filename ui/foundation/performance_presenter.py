from services.performance.models import PerformanceResult
from ui.foundation.models import GuiMetric, GuiSection


class PerformancePresenter:
    """
    Builds display-only performance sections for the GUI.
    """

    def create_sections(self, result: PerformanceResult) -> list[GuiSection]:
        return [
            GuiSection(
                title="Trade Statistics",
                metrics=[
                    GuiMetric("Total Trades", str(result.total_trades)),
                    GuiMetric("Winning Trades", str(result.winning_trades)),
                    GuiMetric("Losing Trades", str(result.losing_trades)),
                    GuiMetric("Win Rate", f"{result.win_rate:.2f}%"),
                ],
            ),
            GuiSection(
                title="Profitability",
                metrics=[
                    GuiMetric("Gross Profit", f"{result.gross_profit:.2f}"),
                    GuiMetric("Gross Loss", f"{result.gross_loss:.2f}"),
                    GuiMetric("Net P/L", f"{result.net_pnl:.2f}"),
                    GuiMetric("Profit Factor", f"{result.profit_factor:.2f}"),
                    GuiMetric("Expectancy", f"{result.expectancy:.2f}"),
                ],
            ),
            GuiSection(
                title="Equity & Drawdown",
                metrics=[
                    GuiMetric("Starting Equity", f"{result.starting_equity:.2f}"),
                    GuiMetric("Ending Equity", f"{result.ending_equity:.2f}"),
                    GuiMetric("Total Return", f"{result.total_return_pct:.2f}%"),
                    GuiMetric("Max Drawdown", f"{result.max_drawdown_pct:.2f}%"),
                ],
            ),
        ]
