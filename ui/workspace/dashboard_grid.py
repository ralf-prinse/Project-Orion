from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.foundation.dashboard_widget_factory import DashboardWidgetFactory
from ui.foundation.models import GuiMetricCard


class DashboardGrid(QWidget):
    """
    Responsive grid containing reusable dashboard widgets.

    Presentation only.

    Widget creation is delegated to DashboardWidgetFactory.
    Layout is driven entirely by GuiMetricCard metadata.
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

        widget = DashboardWidgetFactory.create(
            theme=self.theme,
            card=card,
        )

        self.cards.append(widget)

        index = len(self.cards) - 1

        columns = 3

        row = index // columns
        column = index % columns

        span = max(1, min(card.column_span, columns))

        if span > 1:
            self.layout.addWidget(
                widget,
                row,
                0,
                1,
                span,
            )
            return

        self.layout.addWidget(
            widget,
            row,
            column,
        )

    def add_cards(self, cards: list[GuiMetricCard]):
        for card in cards:
            self.add_card(card)