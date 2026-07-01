from ui.foundation.models import GuiPage
from ui.workspace.models import WorkspacePanel, WorkspaceRegion


class DockManager:
    """
    Deterministic dock-panel manager.

    This is not a Qt docking implementation. It is the presentation model that a
    Qt implementation can consume later.
    """

    def __init__(self, panels: list[WorkspacePanel] | None = None):
        self._panels: dict[str, WorkspacePanel] = {}
        for panel in panels or self.default_panels():
            self.register(panel)

    def register(self, panel: WorkspacePanel) -> None:
        if not panel.panel_id:
            raise ValueError("Workspace panel id cannot be empty")
        if panel.panel_id in self._panels:
            raise ValueError(f"Workspace panel already registered: {panel.panel_id}")
        self._panels[panel.panel_id] = panel

    def replace(self, panel: WorkspacePanel) -> None:
        if not panel.panel_id:
            raise ValueError("Workspace panel id cannot be empty")
        self._panels[panel.panel_id] = panel

    def get(self, panel_id: str) -> WorkspacePanel:
        try:
            return self._panels[panel_id]
        except KeyError as exc:
            raise KeyError(f"Unknown workspace panel: {panel_id}") from exc

    def all_panels(self) -> list[WorkspacePanel]:
        return sorted(self._panels.values(), key=lambda panel: (panel.region.value, panel.order))

    def panels_for_region(self, region: WorkspaceRegion) -> list[WorkspacePanel]:
        return sorted(
            (panel for panel in self._panels.values() if panel.enabled and panel.region == region),
            key=lambda panel: panel.order,
        )

    @staticmethod
    def default_panels() -> list[WorkspacePanel]:
        return [
            WorkspacePanel("dashboard", "Dashboard", GuiPage.DASHBOARD, WorkspaceRegion.CENTRAL, order=10, closable=False),
            WorkspacePanel("scanner", "Scanner", GuiPage.SCANNER, WorkspaceRegion.CENTRAL, order=20, closable=False),
            WorkspacePanel("watchlist", "Watchlist", GuiPage.UNIVERSE, WorkspaceRegion.LEFT_DOCK, order=30),
            WorkspacePanel("portfolio", "Portfolio", GuiPage.PORTFOLIO, WorkspaceRegion.RIGHT_DOCK, order=40),
            WorkspacePanel("performance", "Performance", GuiPage.PERFORMANCE, WorkspaceRegion.BOTTOM_DOCK, order=50),
            WorkspacePanel("logs", "Logs", GuiPage.SETTINGS, WorkspaceRegion.BOTTOM_DOCK, order=90),
        ]
