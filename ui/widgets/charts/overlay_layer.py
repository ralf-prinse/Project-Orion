from __future__ import annotations

from PySide6.QtGui import QPainter

from ui.widgets.charts.chart_layers import ChartLayer, ChartViewport


class OverlayLayer(ChartLayer):
    """
    Base presentation-only overlay layer.

    OverlayLayer reserves a dedicated rendering stage for future
    presentation overlays such as:

    - Trade markers
    - Crosshair
    - Selection
    - Highlighting
    - Indicator overlays
    - Annotations

    This layer intentionally performs no drawing yet. It establishes a
    stable extension point for future visualization components while
    preserving the current rendering pipeline.

    No business logic.
    No trading logic.
    No calculations.
    """

    def draw(
        self,
        painter: QPainter,
        viewport: ChartViewport,
    ) -> None:
        """
        Base implementation.

        Future overlay implementations will override this method.
        """
        return