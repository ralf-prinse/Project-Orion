from PySide6.QtGui import QColor, QPainter, QPen

from ui.design.chart_style import ChartStyle
from ui.widgets.charts.chart_geometry import ChartGeometry


class AxisRenderer:
    """
    Draws chart axes.

    Rendering-only component.
    """

    def draw(
        self,
        painter: QPainter,
        geometry: ChartGeometry,
        style: ChartStyle,
    ):
        pen = QPen(QColor(style.axis_color))
        pen.setWidth(1)

        painter.setPen(pen)

        painter.drawLine(
            geometry.left,
            geometry.top,
            geometry.left,
            geometry.bottom,
        )

        painter.drawLine(
            geometry.left,
            geometry.bottom,
            geometry.right,
            geometry.bottom,
        )