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


class GridLayer(ChartLayer):
    """
    Draws reusable presentation-only chart grid lines.

    GridLayer is part of the ChartCanvas Framework.
    It performs no business logic and consumes no trading data.
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
        point_pen.setWidth(6)
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
        painter.drawText(6, int(viewport.top + 5), f"{maximum:.2f}")
        painter.drawText(6, int(viewport.bottom), f"{minimum:.2f}")