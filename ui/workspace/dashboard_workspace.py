from PySide6.QtWidgets import QPushButton

from ui.foundation.models import GuiSection
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class DashboardWorkspace(BaseWorkspace):
    """
    Presentation-only dashboard workspace.

    Owns the dashboard layout and presentation widgets only.
    Never performs scans, trading logic, portfolio calculations or service
    orchestration.
    """

    def __init__(self, theme, on_scan_requested):
        super().__init__(
            theme=theme,
            title="Goedemorgen Ralf.",
            intro=(
                "Orion zoekt uitsluitend naar kwalitatieve "
                "deterministische swing-trades."
            ),
        )

        self.scan_button = QPushButton("Analyseer markt")
        self.scan_button.clicked.connect(on_scan_requested)
        self.scan_button.setStyleSheet(self.primary_button_style())

        self.market_panel = WorkspacePanel(
            theme=self.theme,
            title="Market Overview",
            body="Nog geen marktupdate beschikbaar.",
        )

        self.opportunities_panel = WorkspacePanel(
            theme=self.theme,
            title="Today's Opportunities",
            body="Nog geen analyse uitgevoerd.",
        )

        self.portfolio_panel = WorkspacePanel(
            theme=self.theme,
            title="Portfolio Snapshot",
            body="Portfolio-overzicht wordt later gekoppeld.",
        )

        self.activity_panel = WorkspacePanel(
            theme=self.theme,
            title="Recent Activity",
            body="Nog geen recente activiteit beschikbaar.",
        )

        self._build_layout()

    def _build_layout(self):
        self.add_workspace_widget(self.scan_button)
        self.add_workspace_widget(self.market_panel)
        self.add_workspace_widget(self.opportunities_panel)
        self.add_workspace_widget(self.portfolio_panel)
        self.add_workspace_widget(self.activity_panel)

    def set_sections(self, sections: list[GuiSection]):
        self.market_panel.setParent(None)
        self.opportunities_panel.setParent(None)
        self.portfolio_panel.setParent(None)
        self.activity_panel.setParent(None)

        for section in sections:
            self.add_workspace_widget(
                WorkspacePanel.from_section(
                    theme=self.theme,
                    section=section,
                )
            )

    def set_status_text(self, text: str):
        self.market_panel.set_body(text)

    def set_advice_html(self, html: str):
        self.opportunities_panel.set_body(html)

    def set_portfolio_snapshot(self, html: str):
        self.portfolio_panel.set_body(html)

    def set_recent_activity(self, html: str):
        self.activity_panel.set_body(html)

    @staticmethod
    def primary_button_style():
        return """
        QPushButton {
            background-color: #2563eb;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
        }
        """