from ui.foundation.models import GuiChartPoint
from ui.widgets.charts.chart_geometry import ChartGeometry


class ChartScaler:
    """
    Converts GuiChartPoint values into screen-space coordinates.

    This class contains rendering math only.
    It performs no portfolio, analytics or trading calculations.
    """

    def scale_points(
        self,
        points: list[GuiChartPoint],
        geometry: ChartGeometry,
    ) -> list[tuple[int, int]]:
        if not points:
            return []

        values = [point.value for point in points]

        min_value = min(values)
        max_value = max(values)
        value_range = max(max_value - min_value, 1)

        scaled_points: list[tuple[int, int]] = []

        for index, point in enumerate(points):
            if len(points) == 1:
                x = geometry.left + geometry.width / 2
            else:
                x = geometry.left + (
                    index / (len(points) - 1)
                ) * geometry.width

            normalized = (point.value - min_value) / value_range
            y = geometry.top + geometry.height - normalized * geometry.height

            scaled_points.append((int(x), int(y)))

        return scaled_points