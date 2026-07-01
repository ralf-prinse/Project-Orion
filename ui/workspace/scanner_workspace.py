from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ScannerWorkspace(QWidget):
    """
    Presentation-only scanner workspace.

    This widget owns the scanner workspace layout and scanner presentation
    widgets. It does not execute scans, call services, calculate signals or
    perform trading logic.
    """

    def __init__(self, theme):
        super().__init__()

        self.theme = theme

        self.summary_label = QLabel("Nog geen scannerresultaten beschikbaar.")
        self.summary_label.setAlignment(Qt.AlignTop)
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            self.theme.muted_text_style() + "; padding: 20px;"
        )

        self._build_layout()

    def _build_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Scanner")
        title.setStyleSheet(self.theme.title_style() + "; margin-top: 25px;")

        intro = QLabel(
            "Bekijk hier de resultaten van marktanalyses en potentiële swing-trade kandidaten."
        )
        intro.setStyleSheet(self.theme.muted_text_style() + "; margin-bottom: 20px;")

        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

    def set_summary_html(self, html: str):
        self.summary_label.setText(html)

    def set_status_text(self, text: str):
        self.summary_label.setText(text)