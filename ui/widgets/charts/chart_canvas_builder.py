from __future__ import annotations

from ui.foundation.charts import GuiChart
from ui.widgets.charts.chart_canvas import ChartCanvas
from ui.widgets.charts.chart_layers import (
    AxisLayer,
    GridLayer,
    LineSeriesLayer,
    ValueLabelLayer,
)
from ui.widgets.charts.overlay_layer import OverlayLayer


class ChartCanvasBuilder:
    """
    Builds reusable presentation-only chart canvases.

    ChartCanvasBuilder owns chart canvas composition.
    It translates GuiChart presentation models into reusable ChartLayer objects.

    No business logic.
    No trading logic.
    No AI logic.
    """

    def build_line_chart_canvas(
        self,
        chart: GuiChart,
        parent=None,
    ) -> ChartCanvas:
        values: list[float] = []

        if chart.series:
            values = chart.series[0].values

        layers = [
            GridLayer(),
            AxisLayer(),
            LineSeriesLayer(values),
            ValueLabelLayer(values),
            OverlayLayer(),
        ]

        return ChartCanvas(
            layers=layers,
            parent=parent,
        )