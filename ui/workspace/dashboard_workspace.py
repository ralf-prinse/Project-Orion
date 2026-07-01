from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class DashboardWorkspace(QWidget):
    """
    Presentation-only dashboard workspace.

    This widget owns the dashboard layout and dashboard presentation widgets.
    It does not perform scans, trading logic, portfolio calculations or service
    orchestration.
    """

    def __init__(self, theme, on_scan_requested):
        super().__init__()

        self.theme = theme
        self.on_scan_requested = on_scan_requested

        self.scan_button = QPushButton("Analyseer markt")
        self.scan_button.clicked.connect(self.on_scan_requested)
        self.scan_button.setStyleSheet(self.primary_button_style())

        self.advice_label = QLabel("Nog geen analyse uitgevoerd.")
        self.advice_label.setAlignment(Qt.AlignTop)
        self.advice_label.setWordWrap(True)
        self.advice_label.setStyleSheet(
            self.theme.muted_text_style() + "; padding: 20px;"
        )

        self._build_layout()

    def _build_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        header = QLabel("Goedemorgen Ralf.")
        header.setStyleSheet(self.theme.title_style() + "; margin-top: 25px;")

        intro = QLabel(
            "Orion zoekt alleen naar concrete swing-trades van enkele uren tot enkele dagen."
        )
        intro.setStyleSheet(self.theme.muted_text_style() + "; margin-bottom: 20px;")

        layout.addWidget(header)
        layout.addWidget(intro)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.advice_label)

        self.setLayout(layout)

    def set_status_text(self, text: str):
        self.advice_label.setText(text)

    def set_advice_html(self, html: str):
        self.advice_label.setText(html)

    def primary_button_style(self):
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