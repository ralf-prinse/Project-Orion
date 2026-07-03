from PySide6.QtWidgets import QApplication

from ui.foundation.chart_models import GuiChartType, GuiSeries
from ui.foundation.charts import GuiChart
from ui.widgets.charts.line_chart_widget import LineChartWidget


def test_line_chart_widget_stores_chart():
    app = QApplication.instance() or QApplication([])

    chart = GuiChart(
        title="Equity Curve",
        subtitle="Portfolio performance",
        chart_type=GuiChartType.LINE,
        series=[
            GuiSeries(
                name="Portfolio",
                values=[100, 110, 120],
            )
        ],
    )

    widget = LineChartWidget(chart)

    assert widget.chart == chart