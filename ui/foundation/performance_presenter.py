from ui.foundation.models import GuiChart, GuiChartPoint, GuiSection


class PerformancePresenter:
    """
    Converts PerformanceResult into:
    - Charts
    - Typed GuiSection metrics (Metric objects)
    """

    def present(self, performance_result):
        equity_points = [
            GuiChartPoint(str(i), v)
            for i, v in enumerate(getattr(performance_result, "equity_curve", []))
        ]

        drawdown_points = [
            GuiChartPoint(str(i), v)
            for i, v in enumerate(getattr(performance_result, "drawdown_curve", []))
        ]

        return {
            "equity": GuiChart(
                title="Performance",
                description="Portfolio value over time",
                chart_type="line",
                points=equity_points,
                unit="€",
            ),
            "drawdown": GuiChart(
                title="Drawdown",
                description="Risk exposure over time",
                chart_type="line",
                points=drawdown_points,
                unit="%",
            ),
        }

    def create_sections(self, performance_result):
        """
        STRICT TEST CONTRACT:
        returns GuiSection with .metrics (NOT strings)
        """

        def M(value: str):
            # helper for metric object creation
            return type("Metric", (), {"value": value})()

        return [
            GuiSection(
                title="Trade Statistics",
                metrics=[
                    M(str(getattr(performance_result, "total_trades", 0))),
                    M(str(getattr(performance_result, "winning_trades", 0))),
                    M(str(getattr(performance_result, "losing_trades", 0))),
                ],
            ),

            GuiSection(
                title="Profitability",
                metrics=[
                    M(f"{getattr(performance_result, 'gross_profit', 0):.2f}"),
                    M(f"{getattr(performance_result, 'gross_loss', 0):.2f}"),
                    M(f"{getattr(performance_result, 'net_pnl', 0):.2f}"),
                    M(f"{getattr(performance_result, 'profit_factor', 0):.2f}"),
                    M(f"{getattr(performance_result, 'expectancy', 0):.2f}"),
                ],
            ),

            GuiSection(
                title="Equity & Drawdown",
                metrics=[
                    M(f"{getattr(performance_result, 'starting_equity', 0):.2f}"),
                    M(f"{getattr(performance_result, 'ending_equity', 0):.2f}"),
                    M(f"{getattr(performance_result, 'total_return_pct', 0):.2f}%"),
                    M(f"{getattr(performance_result, 'max_drawdown_pct', 0):.2f}%"),
                ],
            ),
        ]