from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class ScannerWorkspace(BaseWorkspace):
    """
    Presentation-only scanner workspace.

    This widget owns scanner presentation state and layout. It does not execute
    scans, call services, calculate signals, make decisions or perform trading
    logic.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Scanner",
            intro="Analyseer de markt en bekijk potentiële swing-trade kandidaten.",
        )

        self.theme = theme

        self.status_panel = WorkspacePanel(
            theme=self.theme,
            title="Scan Status",
            body="Scanner gereed.",
        )

        self.results_panel = WorkspacePanel(
            theme=self.theme,
            title="Resultaten",
            body="Nog geen scannerresultaten beschikbaar.",
        )

        self._build_layout()

    def _build_layout(self):

        self.add_workspace_widget(self.status_panel)
        self.add_workspace_widget(self.results_panel)


    def set_status_text(self, text: str):
        self.status_panel.set_body(text)

    def set_summary_html(self, html: str):
        self.results_panel.set_body(html)

    def clear_results(self):
        self.status_panel.set_body("Scanner gereed.")
        self.results_panel.set_body("Nog geen scannerresultaten beschikbaar.")