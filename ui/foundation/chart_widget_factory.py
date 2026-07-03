from __future__ import annotations

from ui.foundation.chart_models import GuiChartType
from ui.foundation.charts import GuiChart
from ui.widgets.charts.line_chart_widget import LineChartWidget


class ChartWidgetFactory:
    """
    Presentation-only chart widget factory.

    Centralizes chart widget selection.

    No business logic.
    No calculations.
    """

    def create_widget(self, chart: GuiChart):
        if chart.chart_type == GuiChartType.LINE:
            return LineChartWidget(chart)

        return None