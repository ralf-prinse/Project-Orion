from PySide6.QtGui import QColor, QFont, QPainter, QPen

from ui.design.chart_style import ChartStyle
from ui.foundation.models import GuiChart
from ui.widgets.charts.chart_geometry import ChartGeometry


class LabelRenderer:
    """
    Draws lightweight chart labels.

    Rendering-only component.
    """

    def draw(
        self,
        painter: QPainter,
        chart: GuiChart,
        geometry: ChartGeometry,
        style: ChartStyle,
    ):
        if not chart.points:
            return

        painter.setPen(QPen(QColor(style.muted_text_color)))

        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)

        first_label = chart.points[0].label
        last_label = chart.points[-1].label

        painter.drawText(
            geometry.left,
            geometry.bottom + 18,
            first_label,
        )

        painter.drawText(
            geometry.right - 80,
            geometry.bottom + 18,
            last_label,
        )

        values = [point.value for point in chart.points]
        min_value = min(values)
        max_value = max(values)

        painter.drawText(
            geometry.left + 8,
            geometry.top + 12,
            f"{max_value:.0f}{chart.unit}",
        )

        painter.drawText(
            geometry.left + 8,
            geometry.bottom - 6,
            f"{min_value:.0f}{chart.unit}",
        )