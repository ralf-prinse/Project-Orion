from PySide6.QtGui import QColor, QPainter, QPen

from ui.design.chart_style import ChartStyle
from ui.widgets.charts.chart_geometry import ChartGeometry


class GridRenderer:
    """
    Draws chart grid lines.

    Rendering-only component.
    """

    def draw(
        self,
        painter: QPainter,
        geometry: ChartGeometry,
        style: ChartStyle,
    ):
        grid_lines = max(style.grid_lines, 1)

        pen = QPen(QColor(style.grid_color))
        pen.setWidth(1)

        painter.setPen(pen)

        for index in range(grid_lines + 1):
            y = geometry.top + int((index / grid_lines) * geometry.height)

            painter.drawLine(
                geometry.left,
                y,
                geometry.right,
                y,
            )