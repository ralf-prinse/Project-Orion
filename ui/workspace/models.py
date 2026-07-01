from dataclasses import dataclass, field
from enum import Enum

from ui.foundation.models import GuiPage


class WorkspaceRegion(str, Enum):
    """
    Stable workspace regions used by the professional desktop shell.

    These regions are toolkit-independent. Qt widgets, future web clients and
    tests can consume the same layout model without importing PySide6.
    """

    SIDEBAR = "sidebar"
    TOOLBAR = "toolbar"
    CENTRAL = "central"
    LEFT_DOCK = "left_dock"
    RIGHT_DOCK = "right_dock"
    BOTTOM_DOCK = "bottom_dock"
    STATUSBAR = "statusbar"


@dataclass(frozen=True)
class WorkspacePanel:
    """
    Presentation-safe description of a panel in the Orion workspace.

    A panel represents a place where existing presenters can render sections.
    It contains no trading logic and no direct backend dependencies.
    """

    panel_id: str
    title: str
    page: GuiPage
    region: WorkspaceRegion = WorkspaceRegion.CENTRAL
    order: int = 100
    enabled: bool = True
    closable: bool = False
    movable: bool = True


@dataclass(frozen=True)
class WorkspaceToolbarAction:
    """
    Display-only toolbar action model.

    Command execution is intentionally not part of the model. The actual GUI
    layer may map actions to callbacks later.
    """

    action_id: str
    label: str
    icon: str = ""
    enabled: bool = True
    order: int = 100


@dataclass(frozen=True)
class WorkspaceStatusItem:
    """
    Stable status-bar item for connection, scan and runtime state.
    """

    key: str
    label: str
    value: str
    order: int = 100


@dataclass
class WorkspaceState:
    """
    Complete deterministic workspace state.

    This object is the single presentation model for the desktop shell. It is
    intentionally small and independent from PySide6 widgets.
    """

    current_page: GuiPage = GuiPage.DASHBOARD
    panels: list[WorkspacePanel] = field(default_factory=list)
    toolbar_actions: list[WorkspaceToolbarAction] = field(default_factory=list)
    status_items: list[WorkspaceStatusItem] = field(default_factory=list)
    active_panel_id: str | None = None

    def enabled_panels(self) -> list[WorkspacePanel]:
        return sorted((panel for panel in self.panels if panel.enabled), key=lambda panel: (panel.region.value, panel.order))

    def panels_for_region(self, region: WorkspaceRegion) -> list[WorkspacePanel]:
        return sorted(
            (panel for panel in self.panels if panel.enabled and panel.region == region),
            key=lambda panel: panel.order,
        )

    def ordered_toolbar_actions(self) -> list[WorkspaceToolbarAction]:
        return sorted((action for action in self.toolbar_actions if action.enabled), key=lambda action: action.order)

    def ordered_status_items(self) -> list[WorkspaceStatusItem]:
        return sorted(self.status_items, key=lambda item: item.order)
