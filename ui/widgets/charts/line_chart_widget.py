from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.foundation.charts import GuiChart


class LineChartWidget(QWidget):
    """
    Presentation-only placeholder Line Chart widget.

    Sprint 4.4 foundation.

    This widget intentionally does not render a real chart yet.
    It renders GuiChart metadata only and will later be upgraded
    to a QtCharts/PyQtGraph implementation.

    No business logic.
    No calculations.
    """

    def __init__(self, chart: GuiChart, parent=None):
        super().__init__(parent)

        self._chart = chart

        layout = QVBoxLayout(self)

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

        point_count = sum(len(series.values) for series in chart.series)

        info = QLabel(
            f"{chart.chart_type.value.upper()} CHART\n\n"
            f"Series: {len(chart.series)}\n"
            f"Points: {point_count}"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(info)
        layout.addStretch()

    @property
    def chart(self) -> GuiChart:
        return self._chart