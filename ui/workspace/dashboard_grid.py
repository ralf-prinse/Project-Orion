from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.workspace.dashboard_card import DashboardCard


class DashboardGrid(QWidget):
    """
    Responsive grid containing reusable DashboardCards.

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

        self.cards: list[DashboardCard] = []

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.cards.clear()

    def add_card(self, card: DashboardCard):
        self.cards.append(card)

        index = len(self.cards) - 1

        columns = 3

        row = index // columns
        column = index % columns

        self.layout.addWidget(card, row, column)

    def add_cards(self, cards: list[DashboardCard]):
        for card in cards:
            self.add_card(card)