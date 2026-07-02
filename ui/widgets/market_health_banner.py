from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from ui.foundation.models import GuiMetricCard


class MarketHealthBanner(QFrame):
    """
    Professional full-width dashboard banner for market health.

    Presentation only.
    Renders a GuiMetricCard model.
    Performs no trading, scanner, portfolio, risk or AI calculations.
    """

    def __init__(self, theme, card: GuiMetricCard):
        super().__init__()

        self.theme = theme
        self.card = card

        self.setObjectName("MarketHealthBanner")
        self.setStyleSheet(self._style(card))

        self.title_label = QLabel(self._title_text(card))
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setStyleSheet(self._title_style(card))

        self.value_label = QLabel(card.value)
        self.value_label.setAlignment(Qt.AlignLeft)
        self.value_label.setStyleSheet(self._value_style())

        self.subtitle_label = QLabel(card.subtitle)
        self.subtitle_label.setAlignment(Qt.AlignLeft)
        self.subtitle_label.setStyleSheet(self._subtitle_style())
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label = QLabel(card.trend)
        self.trend_label.setAlignment(Qt.AlignLeft)
        self.trend_label.setStyleSheet(self._trend_style(card))
        self.trend_label.setVisible(bool(card.trend))

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(10)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.trend_label)

        self.setLayout(layout)

    def set_card(self, card: GuiMetricCard):
        """
        Updates the rendered market health banner.
        """

        self.card = card
        self.setStyleSheet(self._style(card))

        self.title_label.setText(self._title_text(card))
        self.title_label.setStyleSheet(self._title_style(card))

        self.value_label.setText(card.value)

        self.subtitle_label.setText(card.subtitle)
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label.setText(card.trend)
        self.trend_label.setStyleSheet(self._trend_style(card))
        self.trend_label.setVisible(bool(card.trend))

    def _title_text(self, card: GuiMetricCard) -> str:
        if card.icon:
            return f"{card.icon} {card.title.upper()}"

        return card.title.upper()

    def _style(self, card: GuiMetricCard) -> str:
        return f"""
        QFrame#MarketHealthBanner {{
            background-color: {self._background_color(card)};
            border: 1px solid {self._border_color(card)};
            border-radius: 20px;
        }}

        QFrame#MarketHealthBanner:hover {{
            border: 1px solid {self._accent_color(card)};
        }}
        """

    def _title_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: {self._accent_color(card)};
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.6px;
        """

    def _value_style(self) -> str:
        return """
        color: #f9fafb;
        font-size: 34px;
        font-weight: 800;
        """

    def _subtitle_style(self) -> str:
        return """
        color: #d1d5db;
        font-size: 14px;
        font-weight: 600;
        """

    def _trend_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: {self._accent_color(card)};
        font-size: 13px;
        font-weight: 700;
        """

    def _background_color(self, card: GuiMetricCard) -> str:
        if card.status == "success":
            return "#0b2418"

        if card.status == "warning":
            return "#2c1f0b"

        if card.status == "danger":
            return "#2b1010"

        if card.status == "info":
            return "#0c2033"

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