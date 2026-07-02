from PySide6.QtGui import QColor, QPainter, QPen, QBrush

from ui.design.chart_style import ChartStyle


class BarRenderer:
    """
    Renders bar charts for portfolio allocations.

    Pure rendering component.
    """

    def draw(
        self,
        painter: QPainter,
        points: list[tuple[int, int, str]],
        style: ChartStyle,
        geometry,
    ):
        if not points:
            return

        bar_width = max(int(geometry.width / len(points) * 0.6), 4)

        for x, y, label in points:
            height = geometry.bottom - y

            painter.setPen(QPen(QColor(style.primary_line_color)))
            painter.setBrush(QBrush(QColor(style.primary_line_color)))

            painter.drawRect(
                int(x - bar_width / 2),
                int(y),
                bar_width,
                int(height),
            )