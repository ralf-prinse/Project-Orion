from ui.foundation.chart_models import GuiChartType, GuiSeries
from ui.foundation.charts import GuiChart, GuiChartSection


def test_gui_chart_defaults():
    chart = GuiChart(
        title="Equity Curve",
        chart_type=GuiChartType.LINE,
    )

    assert chart.title == "Equity Curve"
    assert chart.chart_type == GuiChartType.LINE
    assert chart.series == []
    assert chart.status == "neutral"
    assert chart.metadata == {}

    assert chart.x_axis.label == ""
    assert chart.y_axis.label == ""

    assert chart.legend.visible is True
    assert chart.legend.position == "bottom"


def test_gui_chart_with_series():
    chart = GuiChart(
        title="Portfolio",
        chart_type=GuiChartType.LINE,
        series=[
            GuiSeries(
                name="Equity",
                values=[100, 110, 120],
                labels=["Jan", "Feb", "Mar"],
            )
        ],
    )

    assert len(chart.series) == 1

    series = chart.series[0]

    assert series.name == "Equity"
    assert series.values == [100, 110, 120]
    assert series.labels == ["Jan", "Feb", "Mar"]


def test_gui_chart_section():
    chart = GuiChart(
        title="Equity Curve",
        chart_type=GuiChartType.LINE,
    )

    section = GuiChartSection(
        title="Performance",
        charts=[chart],
    )

    assert section.title == "Performance"
    assert len(section.charts) == 1
    assert section.charts[0].title == "Equity Curve"
    assert section.metadata == {}