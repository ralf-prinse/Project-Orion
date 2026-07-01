from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.foundation.models import GuiSection


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

    @classmethod
    def from_section(cls, theme, section: GuiSection) -> "WorkspacePanel":
        """
        Creates a WorkspacePanel directly from a GuiSection.

        This keeps rendering responsibilities inside WorkspacePanel and
        eliminates the need for a separate renderer object.
        """
        return cls(
            theme=theme,
            title=section.title,
            body=cls._build_body(section),
        )

    @staticmethod
    def _build_body(section: GuiSection) -> str:
        parts: list[str] = []

        if section.description:
            parts.append(f"<p>{section.description}</p>")

        if section.metrics:
            parts.append("<ul>")

            for metric in section.metrics:
                helper = (
                    f"<br><small>{metric.helper_text}</small>"
                    if metric.helper_text
                    else ""
                )

                parts.append(
                    f"<li><b>{metric.label}:</b> {metric.value}{helper}</li>"
                )

            parts.append("</ul>")

        if not parts:
            return "No information available."

        return "\n".join(parts)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_body(self, text: str):
        self.body_label.setText(text)