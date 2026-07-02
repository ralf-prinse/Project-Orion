from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from ui.foundation.models import GuiMetricCard


class HeroMetricCard(QFrame):
    """
    Large professional KPI card for high-priority dashboard metrics.

    Presentation only.
    Renders GuiMetricCard models.
    Performs no trading, portfolio, scanner, risk or AI calculations.
    """

    def __init__(self, theme, card: GuiMetricCard):
        super().__init__()

        self.theme = theme
        self.card = card

        self.setObjectName("HeroMetricCard")
        self.setStyleSheet(self._style(card))

        self.icon_label = QLabel(card.icon)
        self.icon_label.setAlignment(Qt.AlignLeft)
        self.icon_label.setStyleSheet(self._icon_style(card))
        self.icon_label.setVisible(bool(card.icon))

        self.title_label = QLabel(card.title.upper())
        self.title_label.setStyleSheet(self._title_style(card))

        self.value_label = QLabel(card.value)
        self.value_label.setAlignment(Qt.AlignLeft)
        self.value_label.setStyleSheet(self._value_style(card))

        self.subtitle_label = QLabel(card.subtitle)
        self.subtitle_label.setStyleSheet(self._subtitle_style())
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label = QLabel(card.trend)
        self.trend_label.setStyleSheet(self._trend_style(card))
        self.trend_label.setVisible(bool(card.trend))

        layout = QVBoxLayout()
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(10)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.trend_label)

        self.setLayout(layout)

    def set_card(self, card: GuiMetricCard):
        """
        Updates the rendered hero metric card.
        """

        self.card = card
        self.setStyleSheet(self._style(card))

        self.icon_label.setText(card.icon)
        self.icon_label.setStyleSheet(self._icon_style(card))
        self.icon_label.setVisible(bool(card.icon))

        self.title_label.setText(card.title.upper())
        self.title_label.setStyleSheet(self._title_style(card))

        self.value_label.setText(card.value)
        self.value_label.setStyleSheet(self._value_style(card))

        self.subtitle_label.setText(card.subtitle)
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label.setText(card.trend)
        self.trend_label.setStyleSheet(self._trend_style(card))
        self.trend_label.setVisible(bool(card.trend))

    def _style(self, card: GuiMetricCard) -> str:
        return f"""
        QFrame#HeroMetricCard {{
            background-color: {self._background_color(card)};
            border: 1px solid {self._border_color(card)};
            border-radius: 18px;
        }}

        QFrame#HeroMetricCard:hover {{
            border: 1px solid {self._accent_color(card)};
        }}
        """

    def _icon_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: {self._accent_color(card)};
        font-size: 28px;
        font-weight: bold;
        """

    def _title_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: #9ca3af;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.4px;
        """

    def _value_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: #f9fafb;
        font-size: 36px;
        font-weight: 800;
        """

    def _subtitle_style(self) -> str:
        return """
        color: #d1d5db;
        font-size: 13px;
        font-weight: 500;
        """

    def _trend_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: {self._accent_color(card)};
        font-size: 13px;
        font-weight: 700;
        """

    def _background_color(self, card: GuiMetricCard) -> str:
        if card.status == "success":
            return "#0f2419"

        if card.status == "warning":
            return "#2b1f0d"

        if card.status == "danger":
            return "#2b1111"

        if card.status == "info":
            return "#0f2033"

        return "#111827"

    def _border_color(self, card: GuiMetricCard) -> str:
        if card.accent_color:
            return card.accent_color

        if card.status == "success":
            return "#22c55e"

        if card.status == "warning":
            return "#f59e0b"

        if card.status == "danger":
            return "#ef4444"

        if card.status == "info":
            return "#3b82f6"

        return "#374151"

    def _accent_color(self, card: GuiMetricCard) -> str:
        if card.accent_color:
            return card.accent_color

        if card.status == "success":
            return "#22c55e"

        if card.status == "warning":
            return "#f59e0b"

        if card.status == "danger":
            return "#ef4444"

        if card.status == "info":
            return "#3b82f6"

        return "#9ca3af"