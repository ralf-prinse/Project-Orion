from ui.foundation.models import GuiShellState
from ui.workspace.models import WorkspaceStatusItem


class WorkspaceStatusBar:
    """
    Builds status-bar items from presentation state only.
    """

    def default_items(self) -> list[WorkspaceStatusItem]:
        return [
            WorkspaceStatusItem("connection", "Connection", "Offline", order=10),
            WorkspaceStatusItem("mode", "Mode", "Paper Trading", order=20),
            WorkspaceStatusItem("state", "State", "Ready", order=30),
        ]

    def from_shell_state(self, state: GuiShellState) -> list[WorkspaceStatusItem]:
        return [
            WorkspaceStatusItem("page", "Page", state.current_page.value, order=10),
            WorkspaceStatusItem("status", "Status", state.status_message, order=20),
            WorkspaceStatusItem("sections", "Sections", str(len(state.sections)), order=30),
        ]
