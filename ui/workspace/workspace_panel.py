from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class WorkspacePanel(QWidget):
    """
    Reusable presentation panel for Orion workspaces.

    The panel is responsible only for layout and presentation.
    It contains no business logic and no interaction with services.
    """

    def __init__(
        self,
        theme,
        title: str,
        body: str = "",
    ):
        super().__init__()

        self.theme = theme

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(
            self.theme.title_style() + "; margin-bottom: 12px;"
        )

        self.body_label = QLabel(body)
        self.body_label.setAlignment(Qt.AlignTop)
        self.body_label.setWordWrap(True)
        self.body_label.setStyleSheet(
            self.theme.muted_text_style() + "; padding: 12px;"
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self.title_label)
        layout.addWidget(self.body_label)

        self.setLayout(layout)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_body(self, text: str):
        self.body_label.setText(text)