from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

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
        badge: str | None = None,
    ):
        super().__init__()

        self.theme = theme

        self.container = QFrame()
        self.container.setObjectName("WorkspacePanelContainer")
        self.container.setStyleSheet(self._container_style())

        self.title_label = QLabel(title)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet(
            self.theme.title_style() + "; margin-bottom: 6px;"
        )

        self.badge_label = QLabel(badge or "")
        self.badge_label.setVisible(bool(badge))
        self.badge_label.setStyleSheet(self._badge_style())

        self.body_label = QLabel(body)
        self.body_label.setAlignment(Qt.AlignTop)
        self.body_label.setWordWrap(True)
        self.body_label.setStyleSheet(
            self.theme.muted_text_style() + "; padding-top: 8px;"
        )

        panel_layout = QVBoxLayout()
        panel_layout.setAlignment(Qt.AlignTop)
        panel_layout.setContentsMargins(18, 18, 18, 18)
        panel_layout.setSpacing(8)

        panel_layout.addWidget(self.title_label)
        panel_layout.addWidget(self.badge_label)
        panel_layout.addWidget(self.body_label)

        self.container.setLayout(panel_layout)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.container)

        self.setLayout(root_layout)

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
            parts.append("<div>")

            for metric in section.metrics:
                helper = (
                    f"<br><small>{metric.helper_text}</small>"
                    if metric.helper_text
                    else ""
                )

                parts.append(
                    "<p>"
                    f"<b>{metric.label}</b><br>"
                    f"<span>{metric.value}</span>"
                    f"{helper}"
                    "</p>"
                )

            parts.append("</div>")

        if not parts:
            return "No information available."

        return "\n".join(parts)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_body(self, text: str):
        self.body_label.setText(text)

    def set_badge(self, badge: str | None):
        self.badge_label.setText(badge or "")
        self.badge_label.setVisible(bool(badge))

    def _container_style(self) -> str:
        return """
        QFrame#WorkspacePanelContainer {
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 16px;
        }
        """

    def _badge_style(self) -> str:
        return """
        QLabel {
            background-color: #111827;
            color: #d1d5db;
            border: 1px solid #4b5563;
            border-radius: 10px;
            padding: 4px 10px;
            font-size: 12px;
        }
        """