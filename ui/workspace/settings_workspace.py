from ui.foundation.models import GuiSection
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class SettingsWorkspace(BaseWorkspace):
    """
    Presentation-only settings workspace.

    Displays GuiSections produced by SettingsPresenter.
    The workspace owns layout only and performs no business logic.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Instellingen",
            intro="Bekijk de actieve applicatie-instellingen en configuratie.",
        )

        self._panels: list[WorkspacePanel] = []

    def set_sections(self, sections: list[GuiSection]):
        """
        Render presenter-produced GuiSections.
        """

        # Remove existing panels
        for panel in self._panels:
            panel.setParent(None)

        self._panels.clear()

        # Add new panels
        for section in sections:
            panel = WorkspacePanel.from_section(self.theme, section)
            self._panels.append(panel)
            self.add_workspace_widget(panel)

    def clear(self):
        self.set_sections([])