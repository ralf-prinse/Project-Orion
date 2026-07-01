from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class SettingsWorkspace(BaseWorkspace):
    """
    Presentation-only settings workspace.

    This workspace displays application settings and configuration summaries.
    It does not load providers, mutate configuration or perform business logic.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Instellingen",
            intro="Bekijk de actieve applicatie-instellingen en configuratie.",
        )

        self.settings_panel = WorkspacePanel(
            theme=self.theme,
            title="Actieve instellingen",
            body="Instellingen worden later gekoppeld.",
        )

        self.application_panel = WorkspacePanel(
            theme=self.theme,
            title="Applicatie",
            body="Applicatiegegevens worden later gekoppeld.",
        )

        self._build_layout()

    def _build_layout(self):
        self.add_workspace_widget(self.settings_panel)
        self.add_workspace_widget(self.application_panel)

    def set_settings(self, text: str):
        self.settings_panel.set_body(text)

    def set_application_info(self, text: str):
        self.application_panel.set_body(text)

    def clear(self):
        self.settings_panel.set_body("Instellingen worden later gekoppeld.")
        self.application_panel.set_body("Applicatiegegevens worden later gekoppeld.")