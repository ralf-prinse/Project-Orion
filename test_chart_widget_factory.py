from ui.foundation.chart_models import GuiChartType
from ui.foundation.chart_widget_factory import ChartWidgetFactory
from ui.foundation.charts import GuiChart


def test_chart_widget_factory_returns_none_for_placeholder():
    factory = ChartWidgetFactory()

    chart = GuiChart(
        title="Equity Curve",
        chart_type=GuiChartType.LINE,
    )

    widget = factory.create_widget(chart)

    assert widget is None