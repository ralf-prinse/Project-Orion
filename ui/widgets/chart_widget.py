from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.design.chart_style import ORION_CHART_STYLE
from ui.foundation.models import GuiChart
from ui.widgets.charts.chart_geometry import ChartGeometry
from ui.widgets.charts.chart_renderer import ChartRenderer


class ChartWidget(QWidget):
    """
    ChartWidget 2.0

    Thin orchestration layer only.

    Responsibilities:
    - layout UI (title + description + canvas)
    - delegate rendering to ChartRenderer
    """

    def __init__(self, theme, chart: GuiChart):
        super().__init__()

        self.theme = theme
        self.chart = chart

        self._renderer = ChartRenderer(ORION_CHART_STYLE)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        self.title = QLabel(self.chart.title)
        self.title.setObjectName("chartTitle")

        self.description = QLabel(self.chart.description)
        self.description.setObjectName("chartDescription")
        self.description.setWordWrap(True)

        self.canvas = _ChartCanvas(self.chart, self._renderer)

        layout.addWidget(self.title)

        if self.chart.description:
            layout.addWidget(self.description)

        layout.addWidget(self.canvas)

        self.setLayout(layout)


class _ChartCanvas(QWidget):
    """
    Minimal rendering surface.

    All rendering delegated to ChartRenderer.
    """

    def __init__(self, chart: GuiChart, renderer: ChartRenderer):
        super().__init__()

        self.chart = chart
        self.renderer = renderer

        self.setMinimumHeight(180)

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        margin = 24

        geometry = ChartGeometry(
            left=margin,
            top=margin,
            right=width - margin,
            bottom=height - margin,
        )

        self.renderer.render(
            painter=painter,
            chart=self.chart,
            geometry=geometry,
        )