from PySide6.QtWidgets import QWidget

from ui.foundation.models import GuiMetricCard
from ui.foundation.workspace import GuiWorkspacePanel
from ui.widgets.hero_metric_card import HeroMetricCard
from ui.widgets.market_health_banner import MarketHealthBanner
from ui.widgets.metric_card import MetricCard
from ui.widgets.workspace_panel import WorkspacePanel


class DashboardWidgetFactory:
    """
    Central factory responsible for creating dashboard widgets.

    Supports:
        - Metric cards
        - Workspace panels

    Keeps DashboardGrid independent from concrete widget
    implementations.

    Presentation only.
    """

    @staticmethod
    def create(
        theme,
        card: GuiMetricCard,
    ) -> QWidget:
        """
        Creates the appropriate metric card widget.
        """

        if card.title == "Market Health":
            return MarketHealthBanner(
                theme=theme,
                card=card,
            )

        if card.size == "hero":
            return HeroMetricCard(
                theme=theme,
                card=card,
            )

        return MetricCard(
            theme=theme,
            card=card,
        )

    @staticmethod
    def create_panel(
        theme,
        panel: GuiWorkspacePanel,
    ) -> QWidget:
        """
        Creates a generic workspace panel.

        Presentation only.
        """

        return WorkspacePanel(
            theme=theme,
            panel=panel,
        )