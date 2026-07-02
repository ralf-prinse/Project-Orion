from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from ui.foundation.models import GuiMetricCard


class MetricCard(QFrame):
    """
    Professional reusable KPI card for Orion dashboards.

    Presentation only.
    Renders GuiMetricCard models produced by presenters.
    Performs no trading, portfolio, scanner, risk or AI calculations.
    """

    def __init__(self, theme, card: GuiMetricCard):
        super().__init__()

        self.theme = theme
        self.card = card

        self.setObjectName("MetricCard")
        self.setStyleSheet(self._style(card))

        self.icon_label = QLabel(card.icon)
        self.icon_label.setAlignment(Qt.AlignLeft)
        self.icon_label.setStyleSheet(self._icon_style(card))
        self.icon_label.setVisible(bool(card.icon))

        self.title_label = QLabel(card.title)
        self.title_label.setStyleSheet(self._title_style(card))

        self.value_label = QLabel(card.value)
        self.value_label.setAlignment(Qt.AlignLeft)
        self.value_label.setStyleSheet(self._value_style(card))

        self.subtitle_label = QLabel(card.subtitle)
        self.subtitle_label.setStyleSheet(self._subtitle_style(card))
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label = QLabel(card.trend)
        self.trend_label.setStyleSheet(self._trend_style(card))
        self.trend_label.setVisible(bool(card.trend))

        layout = QVBoxLayout()
        layout.setContentsMargins(*self._margins(card))
        layout.setSpacing(self._spacing(card))

        layout.addWidget(self.icon_label)
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

        self.setStyleSheet(self._style(card))

        self.icon_label.setText(card.icon)
        self.icon_label.setStyleSheet(self._icon_style(card))
        self.icon_label.setVisible(bool(card.icon))

        self.title_label.setText(card.title)
        self.title_label.setStyleSheet(self._title_style(card))

        self.value_label.setText(card.value)
        self.value_label.setStyleSheet(self._value_style(card))

        self.subtitle_label.setText(card.subtitle)
        self.subtitle_label.setStyleSheet(self._subtitle_style(card))
        self.subtitle_label.setVisible(bool(card.subtitle))

        self.trend_label.setText(card.trend)
        self.trend_label.setStyleSheet(self._trend_style(card))
        self.trend_label.setVisible(bool(card.trend))

        if self.layout():
            self.layout().setContentsMargins(*self._margins(card))
            self.layout().setSpacing(self._spacing(card))

    def _style(self, card: GuiMetricCard) -> str:
        border_color = self._border_color(card)
        background_color = self._background_color(card)

        return f"""
        QFrame#MetricCard {{
            background-color: {background_color};
            border: 1px solid {border_color};
            border-radius: 14px;
        }}

        QFrame#MetricCard:hover {{
            border: 1px solid {self._accent_color(card)};
        }}
        """

    def _icon_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: {self._accent_color(card)};
        font-size: {self._icon_font_size(card)}px;
        font-weight: bold;
        """

    def _title_style(self, card: GuiMetricCard) -> str:
        return (
            self.theme.muted_text_style()
            + f"; font-size: {self._title_font_size(card)}px;"
        )

    def _value_style(self, card: GuiMetricCard) -> str:
        return (
            self.theme.title_style()
            + f"; font-size: {self._value_font_size(card)}px; font-weight: bold;"
        )

    def _subtitle_style(self, card: GuiMetricCard) -> str:
        return self.theme.muted_text_style()

    def _trend_style(self, card: GuiMetricCard) -> str:
        return f"""
        color: {self._accent_color(card)};
        font-size: 12px;
        font-weight: 600;
        """

    def _background_color(self, card: GuiMetricCard) -> str:
        if card.status == "success":
            return "#10251b"

        if card.status == "warning":
            return "#2a1f0f"

        if card.status == "danger":
            return "#2a1212"

        if card.status == "info":
            return "#102033"

        return "#1f2937"

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

    def _margins(self, card: GuiMetricCard) -> tuple[int, int, int, int]:
        if card.size == "hero":
            return 24, 24, 24, 24

        if card.size == "compact":
            return 14, 14, 14, 14

        return 18, 18, 18, 18

    def _spacing(self, card: GuiMetricCard) -> int:
        if card.size == "hero":
            return 10

        if card.size == "compact":
            return 6

        return 8

    def _icon_font_size(self, card: GuiMetricCard) -> int:
        if card.size == "hero":
            return 22

        if card.size == "compact":
            return 14

        return 18

    def _title_font_size(self, card: GuiMetricCard) -> int:
        if card.size == "hero":
            return 13

        if card.size == "compact":
            return 11

        return 12

    def _value_font_size(self, card: GuiMetricCard) -> int:
        if card.size == "hero":
            return 32

        if card.size == "compact":
            return 20

        return 24