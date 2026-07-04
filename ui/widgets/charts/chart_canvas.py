from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from ui.widgets.charts.chart_layers import ChartLayer, ChartViewport
from ui.widgets.charts.crosshair_layer import CrosshairLayer


class ChartCanvas(QWidget):
    """
    Core rendering surface.

    Responsibilities:
    - paint lifecycle
    - layer orchestration
    - mouse interaction forwarding

    No business logic.
    No trading calculations.
    No AI calculations.
    """

    def __init__(self, layers: list[ChartLayer], parent=None):
        super().__init__(parent)

        self._layers = layers
        self._viewport = ChartViewport(56, 18, 1, 1)

        self._crosshair_layer = None
        for layer in self._layers:
            if isinstance(layer, CrosshairLayer):
                self._crosshair_layer = layer
                break

        self.setMinimumHeight(280)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self._crosshair_layer:
            pos = event.position()
            self._crosshair_layer.set_mouse_position(
                QPointF(pos.x(), pos.y())
            )
            self.update()

    def leaveEvent(self, event):
        if self._crosshair_layer:
            self._crosshair_layer.set_mouse_position(None)
            self.update()

    def resizeEvent(self, event):
        margin_left = 56
        margin_right = 20
        margin_top = 18
        margin_bottom = 42

        self._viewport = ChartViewport(
            x=margin_left,
            y=margin_top,
            width=max(1, self.width() - margin_left - margin_right),
            height=max(1, self.height() - margin_top - margin_bottom),
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for layer in self._layers:
            try:
                layer.draw(painter, self._viewport)
            except Exception:
                continue