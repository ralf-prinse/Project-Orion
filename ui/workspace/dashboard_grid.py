from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.foundation.models import GuiMetricCard
from ui.widgets.metric_card import MetricCard


class DashboardGrid(QWidget):
    """
    Responsive grid containing reusable MetricCard widgets.

    Presentation only.
    """

    def __init__(self, theme):
        super().__init__()

        self.theme = theme

        self.layout = QGridLayout()
        self.layout.setSpacing(22)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

        self.cards: list[MetricCard] = []

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.cards.clear()

    def add_card(self, card: GuiMetricCard):
        metric_card = MetricCard(
            theme=self.theme,
            card=card,
        )

        self.cards.append(metric_card)

        index = len(self.cards) - 1

        columns = 3

        row = index // columns
        column = index % columns

        self.layout.addWidget(metric_card, row, column)

    def add_cards(self, cards: list[GuiMetricCard]):
        for card in cards:
            self.add_card(card)