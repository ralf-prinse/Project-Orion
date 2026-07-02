from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.foundation.models import GuiMetricCard
from ui.widgets.hero_metric_card import HeroMetricCard
from ui.widgets.metric_card import MetricCard


class DashboardGrid(QWidget):
    """
    Responsive grid containing reusable dashboard widgets.

    Presentation only.

    Hero cards and standard metric cards are selected automatically
    based on the GuiMetricCard presentation model.
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

        if card.size == "hero":
            widget = HeroMetricCard(
                theme=self.theme,
                card=card,
            )
        else:
            widget = MetricCard(
                theme=self.theme,
                card=card,
            )

        self.cards.append(widget)

        index = len(self.cards) - 1

        columns = 3

        row = index // columns
        column = index % columns

        self.layout.addWidget(widget, row, column)

    def add_cards(self, cards: list[GuiMetricCard]):
        for card in cards:
            self.add_card(card)