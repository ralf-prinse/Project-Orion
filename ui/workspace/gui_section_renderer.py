from ui.foundation.models import GuiSection
from ui.workspace.workspace_panel import WorkspacePanel


class GuiSectionRenderer:
    """
    Renders presentation-layer GuiSection objects into workspace panels.

    The renderer is presentation-only. It does not calculate metrics, call
    services, mutate state or perform trading logic.
    """

    def __init__(self, theme):
        self.theme = theme

    def render_section(self, section: GuiSection) -> WorkspacePanel:
        return WorkspacePanel(
            theme=self.theme,
            title=section.title,
            body=self._format_section_body(section),
        )

    def _format_section_body(self, section: GuiSection) -> str:
        parts: list[str] = []

        if section.description:
            parts.append(f"<p>{section.description}</p>")

        if section.metrics:
            parts.append("<ul>")
            for metric in section.metrics:
                helper = f"<br><small>{metric.helper_text}</small>" if metric.helper_text else ""
                parts.append(
                    f"<li><b>{metric.label}:</b> {metric.value}{helper}</li>"
                )
            parts.append("</ul>")

        if not parts:
            return "Geen gegevens beschikbaar."

        return "\n".join(parts)