from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage, GuiShellState
from ui.workspace.dock_manager import DockManager
from ui.workspace.models import WorkspaceState
from ui.workspace.statusbar import WorkspaceStatusBar
from ui.workspace.toolbar import WorkspaceToolbar
from ui.workspace.workspace_layout import WorkspaceLayoutFactory, WorkspaceLayoutSpec


class OrionWorkspace:
    """
    Toolkit-independent professional workspace foundation.

    The workspace composes navigation, panels, toolbar actions and status items.
    It does not create Qt widgets and never performs trading calculations.
    """

    def __init__(
        self,
        shell: GuiShell | None = None,
        dock_manager: DockManager | None = None,
        toolbar: WorkspaceToolbar | None = None,
        statusbar: WorkspaceStatusBar | None = None,
        layout_factory: WorkspaceLayoutFactory | None = None,
    ):
        self.shell = shell or GuiShell()
        self.dock_manager = dock_manager or DockManager()
        self.toolbar = toolbar or WorkspaceToolbar()
        self.statusbar = statusbar or WorkspaceStatusBar()
        self.layout_factory = layout_factory or WorkspaceLayoutFactory()
        self.layout_spec: WorkspaceLayoutSpec = self.layout_factory.create_default()

    def build_state(self) -> WorkspaceState:
        shell_state = self.shell.state
        return self._from_shell_state(shell_state)

    def navigate_to(self, page: GuiPage) -> WorkspaceState:
        shell_state = self.shell.navigate_to(page)
        return self._from_shell_state(shell_state)

    def _from_shell_state(self, shell_state: GuiShellState) -> WorkspaceState:
        panels = self.dock_manager.all_panels()
        active_panel = next((panel for panel in panels if panel.page == shell_state.current_page), None)
        return WorkspaceState(
            current_page=shell_state.current_page,
            panels=panels,
            toolbar_actions=self.toolbar.ordered_actions(),
            status_items=self.statusbar.from_shell_state(shell_state),
            active_panel_id=active_panel.panel_id if active_panel else None,
        )
