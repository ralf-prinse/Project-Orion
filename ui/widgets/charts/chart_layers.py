from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainter, QPen


@dataclass(frozen=True)
class ChartViewport:
    """
    Presentation-only chart viewport.

    Describes the drawable chart area inside a widget.
    """

    x: float
    y: float
    width: float
    height: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def to_rect(self) -> QRectF:
        return QRectF(self.x, self.y, self.width, self.height)


class ChartLayer:
    """
    Base class for presentation-only chart drawing layers.
    """

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        raise NotImplementedError


class GridLayer(ChartLayer):
    """
    Draws reusable presentation-only chart grid lines.
    """

    def __init__(
        self,
        horizontal_lines: int = 4,
        vertical_lines: int = 4,
    ):
        self.horizontal_lines = horizontal_lines
        self.vertical_lines = vertical_lines

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        pen = QPen(Qt.GlobalColor.darkGray)
        pen.setWidth(1)
        painter.setPen(pen)

        if self.horizontal_lines > 0:
            for index in range(1, self.horizontal_lines + 1):
                y = viewport.top + (viewport.height / (self.horizontal_lines + 1)) * index
                painter.drawLine(
                    QPointF(viewport.left, y),
                    QPointF(viewport.right, y),
                )

        if self.vertical_lines > 0:
            for index in range(1, self.vertical_lines + 1):
                x = viewport.left + (viewport.width / (self.vertical_lines + 1)) * index
                painter.drawLine(
                    QPointF(x, viewport.top),
                    QPointF(x, viewport.bottom),
                )


class AxisLayer(ChartLayer):
    """
    Draws basic X/Y chart axes.
    """

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        pen = QPen(Qt.GlobalColor.gray)
        pen.setWidth(1)
        painter.setPen(pen)

        painter.drawLine(
            QPointF(viewport.left, viewport.bottom),
            QPointF(viewport.right, viewport.bottom),
        )

        painter.drawLine(
            QPointF(viewport.left, viewport.bottom),
            QPointF(viewport.left, viewport.top),
        )


class AxisLabelLayer(ChartLayer):
    """
    Draws reusable presentation-only axis labels.

    The layer receives already-prepared presentation values.
    It does not access backend services and contains no trading logic.
    """

    def __init__(
        self,
        values: list[float],
        x_labels: list[str] | None = None,
        y_ticks: int = 4,
        x_ticks: int = 4,
    ):
        self.values = values
        self.x_labels = x_labels or []
        self.y_ticks = y_ticks
        self.x_ticks = x_ticks

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        if not self.values:
            return

        minimum = min(self.values)
        maximum = max(self.values)

        if maximum == minimum:
            maximum = minimum + 1

        painter.setPen(Qt.GlobalColor.gray)

        self._draw_y_labels(
            painter=painter,
            viewport=viewport,
            minimum=minimum,
            maximum=maximum,
        )

        self._draw_x_labels(
            painter=painter,
            viewport=viewport,
        )

    def _draw_y_labels(
        self,
        painter: QPainter,
        viewport: ChartViewport,
        minimum: float,
        maximum: float,
    ) -> None:
        if self.y_ticks <= 0:
            return

        for index in range(self.y_ticks + 1):
            ratio = index / self.y_ticks
            value = maximum - ((maximum - minimum) * ratio)
            y = viewport.top + (viewport.height * ratio)

            painter.drawText(
                int(viewport.left - 52),
                int(y + 4),
                f"{value:.2f}",
            )

    def _draw_x_labels(
        self,
        painter: QPainter,
        viewport: ChartViewport,
    ) -> None:
        value_count = len(self.values)

        if value_count < 2 or self.x_ticks <= 0:
            return

        tick_count = min(self.x_ticks, value_count - 1)

        for index in range(tick_count + 1):
            ratio = index / tick_count
            data_index = round(ratio * (value_count - 1))

            label = str(data_index + 1)

            if self.x_labels and data_index < len(self.x_labels):
                label = str(self.x_labels[data_index])

            x = viewport.left + viewport.width * ratio

            painter.drawText(
                int(x - 10),
                int(viewport.bottom + 22),
                label,
            )


class LineSeriesLayer(ChartLayer):
    """
    Draws a single line series inside the viewport.

    Receives already-determined presentation values.
    No business logic.
    """

    def __init__(self, values: list[float]):
        self.values = values

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        if len(self.values) < 2:
            return

        minimum = min(self.values)
        maximum = max(self.values)

        if maximum == minimum:
            maximum = minimum + 1

        points: list[QPointF] = []

        for index, value in enumerate(self.values):
            x = viewport.left + (index / (len(self.values) - 1)) * viewport.width
            normalized = (value - minimum) / (maximum - minimum)
            y = viewport.bottom - normalized * viewport.height
            points.append(QPointF(x, y))

        line_pen = QPen(Qt.GlobalColor.cyan)
        line_pen.setWidth(3)
        painter.setPen(line_pen)

        for index in range(len(points) - 1):
            painter.drawLine(points[index], points[index + 1])

        point_pen = QPen(Qt.GlobalColor.white)
        point_pen.setWidth(5)
        painter.setPen(point_pen)

        for point in points:
            painter.drawPoint(point)


class ValueLabelLayer(ChartLayer):
    """
    Draws min/max labels for a line chart.
    """

    def __init__(self, values: list[float]):
        self.values = values

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        if not self.values:
            return

        minimum = min(self.values)
        maximum = max(self.values)

        painter.setPen(Qt.GlobalColor.gray)

        painter.drawText(
            int(viewport.right - 72),
            int(viewport.top + 14),
            f"High {maximum:.2f}",
        )

        painter.drawText(
            int(viewport.right - 72),
            int(viewport.bottom - 6),
            f"Low {minimum:.2f}",
        )