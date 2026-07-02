from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.foundation.models import GuiMetricCard
from ui.widgets.hero_metric_card import HeroMetricCard
from ui.widgets.market_health_banner import MarketHealthBanner
from ui.widgets.metric_card import MetricCard


class DashboardGrid(QWidget):
    """
    Responsive grid containing reusable dashboard widgets.

    Presentation only.

    Widget selection is entirely driven by GuiMetricCard metadata.
    """

    def __init__(self, theme):
        super().__init__()

        self.theme = theme

        self.layout = QGridLayout()
        self.layout.setSpacing(22)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

        self.cards: list[QWidget] = []

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.cards.clear()

    def add_card(self, card: GuiMetricCard):

        widget = self._create_widget(card)

        self.cards.append(widget)

        index = len(self.cards) - 1

        columns = 3

        row = index // columns
        column = index % columns

        if isinstance(widget, MarketHealthBanner):
            self.layout.addWidget(widget, row, 0, 1, columns)
            return

        self.layout.addWidget(widget, row, column)

    def add_cards(self, cards: list[GuiMetricCard]):
        for card in cards:
            self.add_card(card)

    def _create_widget(self, card: GuiMetricCard) -> QWidget:
        """
        Factory for dashboard presentation widgets.
        """

        if card.title == "Market Health":
            return MarketHealthBanner(
                theme=self.theme,
                card=card,
            )

        if card.size == "hero":
            return HeroMetricCard(
                theme=self.theme,
                card=card,
            )

        return MetricCard(
            theme=self.theme,
            card=card,
        )