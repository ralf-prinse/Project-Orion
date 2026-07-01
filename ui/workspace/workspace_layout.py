from dataclasses import dataclass

from ui.design import ORION_DARK_THEME, OrionTheme
from ui.workspace.models import WorkspaceRegion


@dataclass(frozen=True)
class WorkspaceLayoutSpec:
    """
    Toolkit-independent layout specification for the Orion desktop shell.
    """

    sidebar_width: int
    toolbar_height: int
    statusbar_height: int
    left_dock_width: int
    right_dock_width: int
    bottom_dock_height: int
    content_margin: int
    panel_gap: int

    def region_minimum_size(self, region: WorkspaceRegion) -> tuple[int, int]:
        if region == WorkspaceRegion.SIDEBAR:
            return (self.sidebar_width, 0)
        if region == WorkspaceRegion.TOOLBAR:
            return (0, self.toolbar_height)
        if region == WorkspaceRegion.STATUSBAR:
            return (0, self.statusbar_height)
        if region == WorkspaceRegion.LEFT_DOCK:
            return (self.left_dock_width, 0)
        if region == WorkspaceRegion.RIGHT_DOCK:
            return (self.right_dock_width, 0)
        if region == WorkspaceRegion.BOTTOM_DOCK:
            return (0, self.bottom_dock_height)
        return (640, 360)


class WorkspaceLayoutFactory:
    """
    Creates stable workspace layout specifications from the design system.
    """

    def __init__(self, theme: OrionTheme | None = None):
        self.theme = theme or ORION_DARK_THEME

    def create_default(self) -> WorkspaceLayoutSpec:
        metrics = self.theme.metrics
        spacing = self.theme.spacing
        return WorkspaceLayoutSpec(
            sidebar_width=metrics.sidebar_width,
            toolbar_height=56,
            statusbar_height=32,
            left_dock_width=280,
            right_dock_width=360,
            bottom_dock_height=240,
            content_margin=spacing.lg,
            panel_gap=spacing.md,
        )
