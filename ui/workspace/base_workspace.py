from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class BaseWorkspace(QWidget):
    """
    Reusable base class for presentation-only Orion workspaces.

    BaseWorkspace owns shared workspace layout concerns such as title,
    introduction text and vertical panel placement. It does not call services,
    execute scans, calculate trading logic or access deterministic engines.
    """

    def __init__(
        self,
        theme,
        title: str,
        intro: str = "",
    ):
        super().__init__()

        self.theme = theme

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(self.theme.title_style() + "; margin-top: 25px;")

        self.intro_label = QLabel(intro)
        self.intro_label.setWordWrap(True)
        self.intro_label.setStyleSheet(
            self.theme.muted_text_style() + "; margin-bottom: 20px;"
        )

        self.layout.addWidget(self.title_label)

        if intro:
            self.layout.addWidget(self.intro_label)

        self.setLayout(self.layout)

    def add_workspace_widget(self, widget: QWidget):
        self.layout.addWidget(widget)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_intro(self, intro: str):
        self.intro_label.setText(intro)
        if self.intro_label.parent() is None:
            self.layout.insertWidget(1, self.intro_label)