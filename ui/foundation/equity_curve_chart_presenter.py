from __future__ import annotations

from ui.foundation.chart_models import (
    GuiAxis,
    GuiChartType,
    GuiLegend,
    GuiSeries,
)
from ui.foundation.charts import GuiChart


class EquityCurveChartPresenter:
    """
    Presentation-only presenter for the dashboard Equity Curve.

    This presenter transforms deterministic equity history into a GuiChart.

    Responsibilities:
        - Create GuiChart objects
        - No calculations
        - No business logic
        - No Qt dependencies
    """

    def present(
        self,
        equity_values: list[float] | None = None,
        labels: list[str] | None = None,
    ) -> GuiChart:
        equity_values = equity_values or []
        labels = labels or []

        return GuiChart(
            title="Equity Curve",
            subtitle="Portfolio performance",
            chart_type=GuiChartType.LINE,
            series=[
                GuiSeries(
                    name="Portfolio",
                    values=equity_values,
                    labels=labels,
                )
            ],
            x_axis=GuiAxis(label="Time"),
            y_axis=GuiAxis(label="Portfolio Value"),
            legend=GuiLegend(
                visible=True,
                position="bottom",
            ),
            status="ready",
            metadata={
                "widget": "equity_curve",
                "version": "4.3",
            },
        )