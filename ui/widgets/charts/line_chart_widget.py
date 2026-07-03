from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.foundation.charts import GuiChart
from ui.widgets.charts.chart_canvas_builder import ChartCanvasBuilder


class LineChartWidget(QWidget):
    """
    Presentation-only Line Chart widget.

    Renders GuiChart metadata and delegates canvas composition
    to ChartCanvasBuilder.

    No business logic.
    No calculations.
    No painting logic.
    """

    def __init__(
        self,
        chart: GuiChart,
        canvas_builder: ChartCanvasBuilder | None = None,
        parent=None,
    ):
        super().__init__(parent)

        self._chart = chart
        self._canvas_builder = canvas_builder or ChartCanvasBuilder()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel(chart.title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        subtitle = QLabel(chart.subtitle)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            color:gray;
        """)

        self.canvas = self._canvas_builder.build_line_chart_canvas(
            chart=chart,
            parent=self,
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.canvas)

    @property
    def chart(self) -> GuiChart:
        return self._chart