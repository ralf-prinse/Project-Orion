from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.foundation.charts import GuiChart
from ui.widgets.charts.chart_canvas_builder import ChartCanvasBuilder


class LineChartWidget(QWidget):
    """
    Presentation-only Line Chart widget.

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

        self.setMinimumHeight(470)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        root_layout = QVBoxLayout(self)
        root_layout.setSpacing(14)
        root_layout.setContentsMargins(16, 16, 16, 16)

        self.container = QFrame()
        self.container.setObjectName("lineChartContainer")
        self.container.setStyleSheet("""
            QFrame#lineChartContainer {
                background-color: #111827;
                border: 1px solid #1f2937;
                border-radius: 16px;
            }
        """)

        container_layout = QVBoxLayout(self.container)
        container_layout.setSpacing(14)
        container_layout.setContentsMargins(18, 18, 18, 18)

        self.canvas = self._canvas_builder.build_line_chart_canvas(
            chart=chart,
            parent=self.container,
        )
        self.canvas.setMinimumHeight(280)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        container_layout.addWidget(self._build_header())
        container_layout.addWidget(self._build_summary())
        container_layout.addWidget(self.canvas, stretch=1)
        container_layout.addWidget(self._build_legend())

        root_layout.addWidget(self.container)

    def _build_header(self) -> QWidget:
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title_block = QWidget()
        title_layout = QVBoxLayout(title_block)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(4)

        title = QLabel(self._chart.title)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("""
            color: #f9fafb;
            font-size: 18px;
            font-weight: bold;
        """)

        subtitle = QLabel(self._chart.subtitle)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle.setStyleSheet("""
            color: #9ca3af;
            font-size: 13px;
        """)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        status = QLabel(self._metadata_text("status_label", "Laatste scan-data"))
        status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        status.setStyleSheet("""
            color: #93c5fd;
            font-size: 12px;
            font-weight: bold;
            padding: 6px 10px;
            border: 1px solid #1d4ed8;
            border-radius: 10px;
            background-color: #1e3a8a;
        """)

        layout.addWidget(title_block, stretch=1)
        layout.addWidget(status)

        return header

    def _build_summary(self) -> QWidget:
        summary = QWidget()
        layout = QGridLayout(summary)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(8)

        items = [
            ("Laatste koers", self._metadata_text("last_value", "-")),
            ("Rendement", self._metadata_text("change_percentage", "-")),
            ("Hoog", self._metadata_text("high_value", "-")),
            ("Laag", self._metadata_text("low_value", "-")),
            ("Datapunten", self._metadata_text("data_points", "-")),
            ("Bron", self._metadata_text("source", "Onbekend")),
        ]

        for index, (label, value) in enumerate(items):
            row = index // 3
            column = index % 3
            layout.addWidget(self._build_summary_item(label, value), row, column)

        return summary

    def _build_summary_item(self, label_text: str, value_text: str) -> QWidget:
        item = QWidget()
        layout = QVBoxLayout(item)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        label = QLabel(label_text)
        label.setStyleSheet("""
            color: #6b7280;
            font-size: 11px;
            font-weight: bold;
        """)

        value = QLabel(value_text)
        value.setStyleSheet("""
            color: #f9fafb;
            font-size: 14px;
            font-weight: bold;
        """)

        layout.addWidget(label)
        layout.addWidget(value)

        return item

    def _build_legend(self) -> QWidget:
        legend = QFrame()
        legend.setObjectName("chartLegend")
        legend.setStyleSheet("""
            QFrame#chartLegend {
                background-color: #0f172a;
                border: 1px solid #1f2937;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        layout = QHBoxLayout(legend)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        series_name = "Series"

        if self._chart.series:
            series_name = self._chart.series[0].name

        label_prefix = QLabel("Legenda:")
        label_prefix.setStyleSheet("""
            color: #f9fafb;
            font-size: 12px;
            font-weight: bold;
        """)

        marker = QLabel("●")
        marker.setStyleSheet("""
            color: #22d3ee;
            font-size: 16px;
            font-weight: bold;
        """)

        label = QLabel(series_name)
        label.setStyleSheet("""
            color: #d1d5db;
            font-size: 12px;
            font-weight: bold;
        """)

        note = QLabel("Close-prijzen uit laatste Yahoo Finance scan")
        note.setStyleSheet("""
            color: #6b7280;
            font-size: 11px;
        """)

        layout.addWidget(label_prefix)
        layout.addWidget(marker)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(note)

        return legend

    def _metadata_text(self, key: str, fallback: str) -> str:
        value = self._chart.metadata.get(key, fallback)

        if value is None:
            return fallback

        return str(value)

    @property
    def chart(self) -> GuiChart:
        return self._chart