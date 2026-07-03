from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from ui.widgets.charts.chart_layers import ChartLayer, ChartViewport


class ChartCanvas(QWidget):
    """
    Reusable presentation-only chart canvas.

    ChartCanvas owns the paint lifecycle and delegates actual drawing
    to composable chart layers.

    No business logic.
    No calculations.
    No trading logic.
    """

    def __init__(self, layers: list[ChartLayer] | None = None, parent=None):
        super().__init__(parent)

        self.layers = layers or []
        self.setMinimumHeight(220)

    def set_layers(self, layers: list[ChartLayer]) -> None:
        self.layers = layers
        self.update()

    def viewport(self) -> ChartViewport:
        margin_left = 44
        margin_right = 24
        margin_top = 24
        margin_bottom = 36

        return ChartViewport(
            x=margin_left,
            y=margin_top,
            width=max(1, self.width() - margin_left - margin_right),
            height=max(1, self.height() - margin_top - margin_bottom),
        )

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        viewport = self.viewport()

        for layer in self.layers:
            layer.draw(painter, viewport)