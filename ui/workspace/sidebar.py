from ui.components import SidebarButtonViewModel, SidebarComponent
from ui.foundation.models import GuiNavigationItem, GuiPage


class WorkspaceSidebar:
    """
    Workspace-level sidebar adapter.

    It reuses the existing SidebarComponent and keeps navigation display logic
    separated from PySide6 widget construction.
    """

    def __init__(self, component: SidebarComponent | None = None):
        self.component = component or SidebarComponent()

    def build_buttons(
        self,
        items: list[GuiNavigationItem],
        current_page: GuiPage,
    ) -> list[SidebarButtonViewModel]:
        return self.component.create_buttons(items, current_page)
