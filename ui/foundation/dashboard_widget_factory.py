from PySide6.QtWidgets import QWidget

from ui.foundation.models import GuiMetricCard
from ui.widgets.hero_metric_card import HeroMetricCard
from ui.widgets.market_health_banner import MarketHealthBanner
from ui.widgets.metric_card import MetricCard


class DashboardWidgetFactory:
    """
    Central factory responsible for creating dashboard widgets.

    The factory keeps DashboardGrid independent from concrete widget
    implementations.

    Presentation only.
    """

    @staticmethod
    def create(
        theme,
        card: GuiMetricCard,
    ) -> QWidget:
        """
        Creates the appropriate dashboard widget.

        Selection is entirely presentation driven.
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