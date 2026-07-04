from __future__ import annotations

from ui.foundation.charts import GuiChart
from ui.widgets.charts.chart_canvas import ChartCanvas
from ui.widgets.charts.chart_layers import (
    AxisLabelLayer,
    AxisLayer,
    GridLayer,
    LineSeriesLayer,
    ValueLabelLayer,
)
from ui.widgets.charts.crosshair_layer import CrosshairLayer
from ui.widgets.charts.overlay_layer import OverlayLayer
from ui.widgets.charts.signal_layer import SignalLayer


class ChartCanvasBuilder:
    """
    Builds reusable presentation-only chart canvases.

    Supports:
    - Grid
    - Axes
    - Axis labels
    - Line series
    - Value labels
    - Crosshair
    - Signals
    - Overlays

    No business logic.
    No trading calculations.
    """

    def build_line_chart_canvas(
        self,
        chart: GuiChart,
        parent=None,
    ) -> ChartCanvas:

        values: list[float] = []
        labels: list[str] = []

        if chart.series:
            values = chart.series[0].values
            labels = chart.series[0].labels

        base_layers = [
            GridLayer(),
            AxisLayer(),
            AxisLabelLayer(
                values=values,
                x_labels=labels,
            ),
            LineSeriesLayer(values),
            ValueLabelLayer(values),
        ]

        crosshair = CrosshairLayer()

        signal_layer = SignalLayer()

        if hasattr(chart, "signals") and chart.signals:
            signal_layer.set_signals(chart.signals)

        overlay_layers = [
            crosshair,
            signal_layer,
            OverlayLayer(),
        ]

        return ChartCanvas(
            layers=base_layers + overlay_layers,
            parent=parent,
        )