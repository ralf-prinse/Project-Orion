from ui.foundation.chart_models import (
    GuiAxis,
    GuiChartType,
    GuiLegend,
    GuiSeries,
)


def test_chart_type_enum():
    assert GuiChartType.LINE.value == "line"
    assert GuiChartType.BAR.value == "bar"
    assert GuiChartType.PIE.value == "pie"
    assert GuiChartType.DONUT.value == "donut"
    assert GuiChartType.AREA.value == "area"


def test_gui_axis_defaults():
    axis = GuiAxis()

    assert axis.label == ""
    assert axis.unit == ""


def test_gui_legend_defaults():
    legend = GuiLegend()

    assert legend.visible is True
    assert legend.position == "bottom"


def test_gui_series_defaults():
    series = GuiSeries(name="Portfolio")

    assert series.name == "Portfolio"
    assert series.values == []
    assert series.labels == []
    assert series.metadata == {}