from ui.foundation.models import GuiChart, GuiChartPoint


class EquityCurvePresenter:
    """
    Converts portfolio history into a GuiChart.
    """

    def present(self, portfolio_history) -> GuiChart:
        points = []

        for snapshot in portfolio_history:
            points.append(
                GuiChartPoint(
                    label=snapshot.date.strftime("%Y-%m-%d"),
                    value=snapshot.total_value,
                )
            )

        return GuiChart(
            title="Equity Curve",
            description="Portfolio performance over time",
            chart_type="line",
            points=points,
            unit="€",
        )