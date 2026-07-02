from PySide6.QtGui import QColor, QPainter, QPen

from ui.design.chart_style import ChartStyle


class LineRenderer:
    """
    Renders a professional line chart.

    Rendering only.
    """

    def draw(
        self,
        painter: QPainter,
        points: list[tuple[int, int]],
        style: ChartStyle,
    ):
        if len(points) < 2:
            return

        pen = QPen(QColor(style.primary_line_color))
        pen.setWidth(2)

        painter.setPen(pen)

        for index in range(len(points) - 1):
            x1, y1 = points[index]
            x2, y2 = points[index + 1]

            painter.drawLine(x1, y1, x2, y2)

        point_pen = QPen(QColor(style.point_color))
        point_pen.setWidth(2)

        painter.setPen(point_pen)

        for x, y in points:
            painter.drawEllipse(x - 3, y - 3, 6, 6)