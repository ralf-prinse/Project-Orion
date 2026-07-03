from PySide6.QtWidgets import QPushButton

from ui.foundation.dashboard_workspace_presenter import DashboardWorkspacePresenter
from ui.foundation.models import GuiMetricCard, GuiSection
from ui.foundation.workspace import GuiWorkspace
from ui.foundation.workspace_renderer import WorkspaceRenderer
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.dashboard_grid import DashboardGrid


class DashboardWorkspace(BaseWorkspace):
    """
    Presentation-only dashboard workspace.

    Owns dashboard presentation widgets only.
    Contains no trading logic, portfolio calculations,
    scanner logic, risk logic or AI decision logic.
    """

    def __init__(self, theme, on_scan_requested):
        super().__init__(
            theme=theme,
            title="Goedemorgen Ralf.",
            intro=(
                "Dashboard 2.0 toont portfolio, marktstatus en scanner-output "
                "op basis van deterministische Orion-resultaten."
            ),
        )

        self.dashboard_workspace_presenter = DashboardWorkspacePresenter()

        self.scan_button = QPushButton("Analyseer markt")
        self.scan_button.clicked.connect(on_scan_requested)
        self.scan_button.setStyleSheet(self.primary_button_style())

        self.dashboard_grid = DashboardGrid(theme=self.theme)
        self.workspace_renderer = WorkspaceRenderer(
            dashboard_grid=self.dashboard_grid
        )

        self._build_layout()

        self.set_workspace(
            self.dashboard_workspace_presenter.create_default_workspace()
        )

    def _build_layout(self):
        self.add_workspace_widget(self.scan_button)
        self.add_workspace_widget(self.dashboard_grid)

    def set_workspace(self, workspace: GuiWorkspace):
        """
        Render a complete dashboard workspace through WorkspaceRenderer.
        """

        self.workspace_renderer.render(workspace)

    def set_cards(self, cards: list[GuiMetricCard]):
        """
        Backward-compatible adapter for existing callers.
        """

        self.set_workspace(
            GuiWorkspace(
                title="Dashboard",
                cards=cards,
            )
        )

    def set_sections(self, sections: list[GuiSection]):
        """
        Compatibility layer for existing GuiSection callers.
        """

        if not sections:
            self.set_workspace(
                self.dashboard_workspace_presenter.create_default_workspace()
            )
            return

        cards: list[GuiMetricCard] = []

        for section in sections:
            metrics = section.metrics or []

            value = metrics[0].value if metrics else ""
            subtitle = (
                " | ".join(
                    f"{metric.label}: {metric.value}"
                    for metric in metrics[1:]
                )
                if len(metrics) > 1
                else section.description
            )

            cards.append(
                GuiMetricCard(
                    title=section.title,
                    value=value,
                    subtitle=subtitle,
                    trend=section.description,
                )
            )

        self.set_cards(cards)

    def set_status_text(self, text: str):
        self.set_cards(
            [
                GuiMetricCard(
                    title="Market Overview",
                    value="Status",
                    subtitle=text,
                    trend="Laatste dashboardmelding.",
                )
            ]
        )

    def primary_button_style(self):
        return """
        QPushButton {
            background-color: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            padding: 15px 18px;
            border-radius: 14px;
            margin-bottom: 22px;
            border: 1px solid #3b82f6;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
            border: 1px solid #60a5fa;
        }

        QPushButton:pressed {
            background-color: #1e40af;
        }
        """