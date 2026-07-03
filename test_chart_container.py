from PySide6.QtWidgets import QApplication, QLabel

from ui.workspace.chart_container import ChartContainer


def test_chart_container_adds_widgets():
    app = QApplication.instance() or QApplication([])

    container = ChartContainer()

    widget = QLabel("Equity Curve")

    container.add_chart_widget(widget)

    assert len(container.widgets) == 1
    assert container.widgets[0] == widget
    assert container.layout.count() == 1


def test_chart_container_clears_widgets():
    app = QApplication.instance() or QApplication([])

    container = ChartContainer()

    widget = QLabel("Equity Curve")
    container.add_chart_widget(widget)

    container.clear()

    assert container.widgets == []
    assert container.layout.count() == 0