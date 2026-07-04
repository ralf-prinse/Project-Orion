from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPen

from ui.widgets.charts.chart_layers import ChartLayer, ChartViewport


class CrosshairLayer(ChartLayer):
    """
    Interactive crosshair overlay layer.

    Purpose:
    - Visual cursor guidance
    - Future support for hover inspection
    - Foundation for trading interaction UX

    No business logic.
    No calculations.
    """

    def __init__(self):
        self._mouse_pos: QPointF | None = None

    def set_mouse_position(self, pos: QPointF | None) -> None:
        self._mouse_pos = pos

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        if self._mouse_pos is None:
            return

        pen = QPen(Qt.GlobalColor.lightGray)
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setWidth(1)

        painter.setPen(pen)

        # Vertical line
        painter.drawLine(
            QPointF(self._mouse_pos.x(), viewport.top),
            QPointF(self._mouse_pos.x(), viewport.bottom),
        )

        # Horizontal line
        painter.drawLine(
            QPointF(viewport.left, self._mouse_pos.y()),
            QPointF(viewport.right, self._mouse_pos.y()),
        )