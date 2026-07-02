from PySide6.QtGui import QPainter, QPen, QColor

from ui.design.chart_style import ChartStyle
from ui.widgets.charts.chart_geometry import ChartGeometry


class ChartRenderer:
    """
    Advanced Chart Renderer supporting:

    - Line charts (single series)
    - Multi-line overlays (benchmark vs portfolio)
    """

    def __init__(self, style: ChartStyle):
        self._style = style

    def render(self, painter: QPainter, chart, geometry: ChartGeometry):

        if not chart:
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # ----------------------------
        # 1. MULTI-LINE CHART (NEW)
        # ----------------------------
        if hasattr(chart, "overlays") and chart.overlays:

            colors = {
                "portfolio": QColor("#00d4ff"),
                "benchmark": QColor("#ffb020"),
            }

            for key, series in chart.overlays.items():

                if not series:
                    continue

                pen = QPen(colors.get(key, QColor("#ffffff")))
                pen.setWidth(2)
                painter.setPen(pen)

                self._draw_line(painter, series, geometry)

        # ----------------------------
        # 2. SINGLE LINE FALLBACK
        # ----------------------------
        elif chart.points:
            pen = QPen(QColor(self._style.primary_line_color))
            pen.setWidth(2)
            painter.setPen(pen)

            self._draw_line(painter, chart.points, geometry)

    # ----------------------------
    # INTERNAL DRAW METHOD
    # ----------------------------
    def _draw_line(self, painter, points, geometry: ChartGeometry):

        if not points:
            return

        values = [p.value for p in points]

        if not values:
            return

        min_v = min(values)
        max_v = max(values)
        range_v = max_v - min_v if max_v != min_v else 1

        width = geometry.right - geometry.left
        height = geometry.bottom - geometry.top

        step_x = width / max(len(points) - 1, 1)

        prev_x = geometry.left
        prev_y = geometry.bottom - ((values[0] - min_v) / range_v) * height

        for i in range(1, len(points)):
            x = geometry.left + i * step_x
            y = geometry.bottom - ((values[i] - min_v) / range_v) * height

            painter.drawLine(int(prev_x), int(prev_y), int(x), int(y))

            prev_x = x
            prev_y = y