from PySide6.QtWidgets import QApplication

from ui.widgets.charts.chart_canvas import ChartCanvas
from ui.widgets.charts.chart_layers import ChartViewport


class DummyLayer:
    def __init__(self):
        self.draw_called = False
        self.viewport = None

    def draw(self, painter, viewport):
        self.draw_called = True
        self.viewport = viewport


def test_chart_canvas_stores_layers():
    app = QApplication.instance() or QApplication([])

    layer = DummyLayer()
    canvas = ChartCanvas(layers=[layer])

    assert canvas.layers == [layer]


def test_chart_canvas_set_layers():
    app = QApplication.instance() or QApplication([])

    first = DummyLayer()
    second = DummyLayer()

    canvas = ChartCanvas(layers=[first])
    canvas.set_layers([second])

    assert canvas.layers == [second]


def test_chart_canvas_viewport_returns_chart_viewport():
    app = QApplication.instance() or QApplication([])

    canvas = ChartCanvas()

    viewport = canvas.viewport()

    assert isinstance(viewport, ChartViewport)
    assert viewport.width >= 1
    assert viewport.height >= 1