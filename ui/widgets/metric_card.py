from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from ui.foundation.models import GuiMetricCard


class MetricCard(QFrame):
    """
    Professional KPI card for Orion dashboards.

    Displays a single highlighted metric. The widget performs no calculations
    and simply renders a GuiMetricCard produced by presenters.
    """

    def __init__(self, theme, card: GuiMetricCard):
        super().__init__()

        self.theme = theme
        self.card = card

        self.setObjectName("MetricCard")
        self.setStyleSheet(self._style())

        self.title_label = QLabel(card.title)
        self.title_label.setStyleSheet(
            self.theme.muted_text_style() + "; font-size: 12px;"
        )

        self.value_label = QLabel(card.value)
        self.value_label.setAlignment(Qt.AlignLeft)
        self.value_label.setStyleSheet(
            self.theme.title_style() + "; font-size: 24px; font-weight: bold;"
        )

        self.subtitle_label = QLabel(card.subtitle)
        self.subtitle_label.setStyleSheet(self.theme.muted_text_style())
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label = QLabel(card.trend)
        self.trend_label.setStyleSheet(self.theme.muted_text_style())
        self.trend_label.setVisible(bool(card.trend))

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.trend_label)

        self.setLayout(layout)

    def set_card(self, card: GuiMetricCard):
        """
        Updates the rendered metric card.
        """

        self.card = card

        self.title_label.setText(card.title)
        self.value_label.setText(card.value)

        self.subtitle_label.setText(card.subtitle)
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label.setText(card.trend)
        self.trend_label.setVisible(bool(card.trend))

    def _style(self) -> str:
        return """
        QFrame#MetricCard {
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 14px;
        }
        """