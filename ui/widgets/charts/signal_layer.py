from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen

from ui.widgets.charts.chart_layers import ChartLayer, ChartViewport


class SignalLayer(ChartLayer):
    """
    Presentation-only signal overlay layer.

    Purpose:
    - Visual representation of trading signals (BUY / SELL markers)
    - Prepared for future integration with TradingPipeline output
    - Pure rendering layer (no logic)

    No business logic.
    No calculations.
    """

    def __init__(self):
        # List of signals in viewport coordinates
        self._signals: list[tuple[float, float, str]] = []

    def set_signals(self, signals: list[tuple[float, float, str]]) -> None:
        """
        signals format:
        (x, y, type)
        type = "BUY" | "SELL"
        """
        self._signals = signals

    def draw(self, painter: QPainter, viewport: ChartViewport) -> None:
        if not self._signals:
            return

        for x, y, signal_type in self._signals:

            if signal_type == "BUY":
                pen = QPen(Qt.GlobalColor.green)
            else:
                pen = QPen(Qt.GlobalColor.red)

            pen.setWidth(2)
            painter.setPen(pen)

            # simple marker cross
            painter.drawLine(x - 5, y - 5, x + 5, y + 5)
            painter.drawLine(x - 5, y + 5, x + 5, y - 5)