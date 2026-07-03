from ui.foundation.chart_models import GuiChartType
from ui.foundation.chart_renderer import ChartRenderer
from ui.foundation.charts import GuiChart


class DummyChartWidgetFactory:
    def create_widget(self, chart):
        return {
            "widget": "line_chart",
            "title": chart.title,
        }


def test_chart_renderer_returns_widgets_for_charts():
    renderer = ChartRenderer(
        chart_widget_factory=DummyChartWidgetFactory()
    )

    charts = [
        GuiChart(
            title="Equity Curve",
            chart_type=GuiChartType.LINE,
        )
    ]

    widgets = renderer.render(charts)

    assert len(widgets) == 1
    assert widgets[0]["widget"] == "line_chart"
    assert widgets[0]["title"] == "Equity Curve"


def test_chart_renderer_skips_unknown_chart_widgets():
    class UnknownChartWidgetFactory:
        def create_widget(self, chart):
            return None

    renderer = ChartRenderer(
        chart_widget_factory=UnknownChartWidgetFactory()
    )

    charts = [
        GuiChart(
            title="Unknown Chart",
            chart_type=GuiChartType.LINE,
        )
    ]

    widgets = renderer.render(charts)

    assert widgets == []