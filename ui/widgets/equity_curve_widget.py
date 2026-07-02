from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from ui.foundation.models import GuiChart


class EquityCurveCanvas(QWidget):
    """
    Lightweight equity curve canvas.

    Presentation only.
    Draws GuiChart points.
    """

    def __init__(self, chart: GuiChart):
        super().__init__()

        self.chart = chart
        self.setMinimumHeight(160)

    def set_chart(self, chart: GuiChart):
        self.chart = chart
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.chart.points:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        padding = 18

        values = [point.value for point in self.chart.points]

        min_value = min(values)
        max_value = max(values)

        if min_value == max_value:
            min_value -= 1
            max_value += 1

        drawable_width = max(width - padding * 2, 1)
        drawable_height = max(height - padding * 2, 1)

        points: list[QPointF] = []

        for index, value in enumerate(values):
            x = padding

            if len(values) > 1:
                x += (index / (len(values) - 1)) * drawable_width

            normalized = (value - min_value) / (max_value - min_value)
            y = padding + (1 - normalized) * drawable_height

            points.append(QPointF(x, y))

        grid_pen = QPen(Qt.GlobalColor.darkGray)
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)

        for i in range(4):
            y = padding + (i / 3) * drawable_height
            painter.drawLine(
                padding,
                int(y),
                width - padding,
                int(y),
            )

        line_pen = QPen(Qt.GlobalColor.white)
        line_pen.setWidth(3)
        painter.setPen(line_pen)

        for index in range(len(points) - 1):
            painter.drawLine(points[index], points[index + 1])

        dot_pen = QPen(Qt.GlobalColor.white)
        dot_pen.setWidth(6)
        painter.setPen(dot_pen)

        for point in points:
            painter.drawPoint(point)


class EquityCurveWidget(QFrame):
    """
    Professional dashboard widget for equity curve visualization.

    Presentation only.
    Performs no trading, portfolio, scanner, risk or AI calculations.
    """

    def __init__(self, theme, chart: GuiChart):
        super().__init__()

        self.theme = theme
        self.chart = chart

        self.setObjectName("EquityCurveWidget")
        self.setStyleSheet(self._style())

        self.title_label = QLabel(chart.title)
        self.title_label.setStyleSheet(self._title_style())

        self.description_label = QLabel(chart.description)
        self.description_label.setStyleSheet(self._description_style())
        self.description_label.setVisible(bool(chart.description))

        self.canvas = EquityCurveCanvas(chart)

        layout = QVBoxLayout()
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(12)

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def set_chart(self, chart: GuiChart):
        self.chart = chart

        self.title_label.setText(chart.title)

        self.description_label.setText(chart.description)
        self.description_label.setVisible(bool(chart.description))

        self.canvas.set_chart(chart)

    def _style(self) -> str:
        return """
        QFrame#EquityCurveWidget {
            background-color: #111827;
            border: 1px solid #374151;
            border-radius: 18px;
        }

        QFrame#EquityCurveWidget:hover {
            border: 1px solid #3b82f6;
        }
        """

    def _title_style(self) -> str:
        return """
        color: #f9fafb;
        font-size: 16px;
        font-weight: 800;
        """

    def _description_style(self) -> str:
        return """
        color: #9ca3af;
        font-size: 12px;
        font-weight: 500;
        """