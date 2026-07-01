from ui.foundation.models import GuiSection
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class HistoryWorkspace(BaseWorkspace):
    """
    Presentation-only history workspace.

    Displays deterministic trade history produced by Orion services.
    Never performs calculations or interacts with trading logic.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Historie",
            intro="Bekijk de uitgevoerde trades en recente handelsactiviteiten.",
        )

        self.history_panel = WorkspacePanel(
            theme=self.theme,
            title="Trade History",
            body="Er zijn nog geen trade-events beschikbaar.",
        )

        self.statistics_panel = WorkspacePanel(
            theme=self.theme,
            title="Samenvatting",
            body="Statistieken worden later gekoppeld.",
        )

        self._build_layout()

    def _build_layout(self):
        self.add_workspace_widget(self.history_panel)
        self.add_workspace_widget(self.statistics_panel)

    def set_sections(self, sections: list[GuiSection]):
        self.history_panel.setParent(None)
        self.statistics_panel.setParent(None)

        for section in sections:
            self.add_workspace_widget(
                WorkspacePanel.from_section(
                    theme=self.theme,
                    section=section,
                )
            )

    # Legacy API (temporary during migration)

    def set_history(self, text: str):
        self.history_panel.set_body(text)

    def set_statistics(self, text: str):
        self.statistics_panel.set_body(text)

    def clear(self):
        self.history_panel.set_body(
            "Er zijn nog geen trade-events beschikbaar."
        )
        self.statistics_panel.set_body(
            "Statistieken worden later gekoppeld."
        )