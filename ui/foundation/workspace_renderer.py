from __future__ import annotations

from ui.foundation.chart_renderer import ChartRenderer
from ui.foundation.workspace import GuiWorkspace
from ui.workspace.chart_container import ChartContainer
from ui.workspace.dashboard_grid import DashboardGrid


class WorkspaceRenderer:
    """
    Presentation-only workspace renderer.

    Renders GuiWorkspace content into existing desktop layout infrastructure.

    Responsibilities:
        - render cards through DashboardGrid
        - render charts through ChartRenderer
        - place chart widgets into ChartContainer

    No business logic.
    No calculations.
    """

    def __init__(
        self,
        dashboard_grid: DashboardGrid,
        chart_container: ChartContainer,
        chart_renderer: ChartRenderer | None = None,
    ) -> None:
        self._dashboard_grid = dashboard_grid
        self._chart_container = chart_container
        self._chart_renderer = (
            chart_renderer
            if chart_renderer is not None
            else ChartRenderer()
        )

    def render(self, workspace: GuiWorkspace) -> None:
        self._dashboard_grid.clear()
        self._dashboard_grid.add_cards(workspace.cards)

        self._chart_container.clear()
        chart_widgets = self._chart_renderer.render(workspace.charts)
        self._chart_container.add_chart_widgets(chart_widgets)