from __future__ import annotations

from ui.foundation.workspace import GuiWorkspace, GuiWorkspacePanel
from ui.foundation.workspace_renderer import WorkspaceRenderer
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.chart_container import ChartContainer
from ui.workspace.dashboard_grid import DashboardGrid


class TradingDashboardWorkspace(BaseWorkspace):
    """
    Main Orion Trading Dashboard workspace.

    Presentation only.

    This workspace renders dashboard presentation models through
    the generic WorkspaceRenderer infrastructure.

    It contains NO business logic.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Trading Dashboard",
            intro="Live overzicht van de autonome paper trading lifecycle.",
        )

        self.dashboard_grid = DashboardGrid(theme=self.theme)
        self.chart_container = ChartContainer()

        self.workspace_renderer = WorkspaceRenderer(
            dashboard_grid=self.dashboard_grid,
            chart_container=self.chart_container,
        )

        self.add_workspace_widget(self.dashboard_grid)
        self.add_workspace_widget(self.chart_container)

        self.set_status_text("Dashboard gereed. Klik op refresh om data te laden.")

    def set_workspace(
        self,
        workspace: GuiWorkspace,
    ) -> None:
        self.workspace_renderer.render(workspace)

    def set_status_text(
        self,
        text: str,
    ) -> None:
        self.set_workspace(
            GuiWorkspace(
                title="Trading Dashboard",
                subtitle="Status",
                panels=[
                    GuiWorkspacePanel(
                        panel_type="dashboard_status",
                        title="Status",
                        subtitle=text,
                        items=[],
                        status="info",
                        metadata={},
                    )
                ],
                metadata={},
            )
        )