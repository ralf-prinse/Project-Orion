from PySide6.QtWidgets import QPushButton

from ui.foundation.dashboard_2_presenter import Dashboard2Presenter
from ui.foundation.dashboard_card_model import DashboardCardModel
from ui.foundation.models import GuiSection
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.dashboard_card import DashboardCard
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

        self.dashboard_2_presenter = Dashboard2Presenter()

        self.scan_button = QPushButton("Analyseer markt")
        self.scan_button.clicked.connect(on_scan_requested)
        self.scan_button.setStyleSheet(self.primary_button_style())

        self.dashboard_grid = DashboardGrid(theme=self.theme)

        self._build_layout()
        self.set_cards(self.dashboard_2_presenter.create_default_cards())

    def _build_layout(self):
        self.add_workspace_widget(self.scan_button)
        self.add_workspace_widget(self.dashboard_grid)

    def set_cards(self, cards: list[DashboardCardModel]):
        self.dashboard_grid.clear()

        for card in cards:
            self.dashboard_grid.add_card(
                DashboardCard(
                    theme=self.theme,
                    title=card.title,
                    value=card.value,
                    subtitle=card.subtitle,
                    footer=card.footer,
                )
            )

    def set_sections(self, sections: list[GuiSection]):
        """
        Compatibility layer for existing GuiSection callers.
        """

        if not sections:
            self.set_cards(self.dashboard_2_presenter.create_default_cards())
            return

        cards: list[DashboardCardModel] = []

        for section in sections:
            metrics = section.metrics or []

            if metrics:
                value = metrics[0].value
                subtitle = " | ".join(
                    f"{metric.label}: {metric.value}"
                    for metric in metrics[1:]
                )
            else:
                value = ""
                subtitle = section.description

            cards.append(
                DashboardCardModel(
                    title=section.title,
                    value=value,
                    subtitle=subtitle,
                    footer=section.description,
                )
            )

        self.set_cards(cards)

    def set_status_text(self, text: str):
        self.set_cards(
            [
                DashboardCardModel(
                    title="Market Overview",
                    value="Status",
                    subtitle=text,
                    footer="Laatste dashboardmelding.",
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