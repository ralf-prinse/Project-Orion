from __future__ import annotations

from dataclasses import dataclass

from ui.foundation.models import GuiPage
from ui.workspace.models import WorkspaceState


@dataclass(frozen=True)
class WorkspaceControllerResult:
    """Result returned after a workspace navigation action."""

    state: WorkspaceState
    changed: bool


class WorkspaceController:
    """
    Coordinates workspace navigation state.

    The controller is intentionally GUI-framework independent.
    It does not create widgets, perform trading logic or access services.
    """

    def __init__(self, initial_page: GuiPage = GuiPage.DASHBOARD) -> None:
        self._current_page = initial_page

    @property
    def current_page(self) -> GuiPage:
        return self._current_page

    def navigate_to(self, page: GuiPage) -> WorkspaceControllerResult:
        changed = page != self._current_page
        self._current_page = page

        return WorkspaceControllerResult(
            state=self.current_state(),
            changed=changed,
        )

    def current_state(self) -> WorkspaceState:
        return WorkspaceState(
            current_page=self._current_page,
            active_panel_id=self._current_page.value,
        )