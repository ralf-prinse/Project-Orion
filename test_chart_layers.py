from ui.widgets.charts.chart_layers import (
    ChartViewport,
    GridLayer,
    LineSeriesLayer,
    ValueLabelLayer,
)


def test_chart_viewport_boundaries():
    viewport = ChartViewport(
        x=10,
        y=20,
        width=300,
        height=200,
    )

    assert viewport.left == 10
    assert viewport.top == 20
    assert viewport.right == 310
    assert viewport.bottom == 220


def test_grid_layer_defaults():
    layer = GridLayer()

    assert layer.horizontal_lines == 4
    assert layer.vertical_lines == 4


def test_line_series_layer_stores_values():
    layer = LineSeriesLayer(values=[100, 110, 120])

    assert layer.values == [100, 110, 120]


def test_value_label_layer_stores_values():
    layer = ValueLabelLayer(values=[100, 110, 120])

    assert layer.values == [100, 110, 120]