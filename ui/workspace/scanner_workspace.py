from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.workspace.workspace_panel import WorkspacePanel


class ScannerWorkspace(QWidget):
    """
    Presentation-only scanner workspace.

    This widget owns scanner presentation state and layout. It does not execute
    scans, call services, calculate signals, make decisions or perform trading
    logic.
    """

    def __init__(self, theme):
        super().__init__()

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
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Scanner")
        title.setStyleSheet(self.theme.title_style() + "; margin-top: 25px;")

        intro = QLabel(
            "Analyseer de markt en bekijk potentiële swing-trade kandidaten."
        )
        intro.setStyleSheet(self.theme.muted_text_style() + "; margin-bottom: 20px;")

        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(self.status_panel)
        layout.addWidget(self.results_panel)

        self.setLayout(layout)

    def set_status_text(self, text: str):
        self.status_panel.set_body(text)

    def set_summary_html(self, html: str):
        self.results_panel.set_body(html)

    def clear_results(self):
        self.status_panel.set_body("Scanner gereed.")
        self.results_panel.set_body("Nog geen scannerresultaten beschikbaar.")