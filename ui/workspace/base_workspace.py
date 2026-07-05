from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


class BaseWorkspace(QScrollArea):
    """
    Reusable base class for presentation-only Orion workspaces.

    Provides a stable scrollable content area so workspace content never
    falls outside the visible desktop window after resize, maximize or
    dynamic content updates.
    """

    def __init__(
        self,
        theme,
        title: str,
        intro: str = "",
    ):
        super().__init__()

        self.theme = theme

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        self.content = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(16)

        self.title_label = QLabel(title)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(
            self.theme.title_style() + "; margin-top: 0px;"
        )

        self.intro_label = QLabel(intro)
        self.intro_label.setWordWrap(True)
        self.intro_label.setStyleSheet(
            self.theme.muted_text_style() + "; margin-bottom: 10px;"
        )

        self.layout.addWidget(self.title_label)

        if intro:
            self.layout.addWidget(self.intro_label)

        self.content.setLayout(self.layout)
        self.setWidget(self.content)

    def add_workspace_widget(self, widget: QWidget):
        self.layout.addWidget(widget)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_intro(self, intro: str):
        self.intro_label.setText(intro)
        if self.intro_label.parent() is None:
            self.layout.insertWidget(1, self.intro_label)