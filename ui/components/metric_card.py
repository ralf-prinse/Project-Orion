from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class MetricCard(QWidget):
    """
    Reusable professional UI card for displaying one important metric.

    Presentation only.
    No business logic.
    """

    def __init__(
        self,
        theme,
        title: str,
        value: str,
        subtitle: str = "",
        variant: str = "default",
    ):
        super().__init__()

        self.theme = theme
        self.variant = variant

        self.title_label = QLabel(title)
        self.value_label = QLabel(value)
        self.subtitle_label = QLabel(subtitle)

        self.title_label.setStyleSheet(self._title_style())
        self.value_label.setStyleSheet(self._value_style())
        self.subtitle_label.setStyleSheet(self._subtitle_style())

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)

        self.setLayout(layout)
        self.setStyleSheet(self._card_style())

    def set_value(self, value: str):
        self.value_label.setText(value)
        self._auto_variant_from_value(value)
        self._refresh_styles()

    def set_subtitle(self, subtitle: str):
        self.subtitle_label.setText(subtitle)

    def set_variant(self, variant: str):
        self.variant = variant
        self._refresh_styles()

    def _auto_variant_from_value(self, value: str):
        normalized = value.strip().upper()

        if normalized == "BUY":
            self.variant = "success"
        elif normalized == "SELL":
            self.variant = "danger"
        elif normalized == "HOLD":
            self.variant = "warning"

    def _refresh_styles(self):
        self.setStyleSheet(self._card_style())
        self.value_label.setStyleSheet(self._value_style())

    def _card_style(self):
        border_color = self._border_color()
        background_color = "#1f2937"

        return f"""
        QWidget {{
            background-color: {background_color};
            border: 1px solid {border_color};
            border-radius: 16px;
            margin-bottom: 12px;
        }}
        """

    def _title_style(self):
        return """
        QLabel {
            color: #9ca3af;
            font-size: 13px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        """

    def _value_style(self):
        return f"""
        QLabel {{
            color: {self._value_color()};
            font-size: 30px;
            font-weight: bold;
        }}
        """

    def _subtitle_style(self):
        return """
        QLabel {
            color: #d1d5db;
            font-size: 13px;
        }
        """

    def _border_color(self):
        if self.variant == "success":
            return "#22c55e"

        if self.variant == "danger":
            return "#ef4444"

        if self.variant == "warning":
            return "#f59e0b"

        return "#374151"

    def _value_color(self):
        if self.variant == "success":
            return "#22c55e"

        if self.variant == "danger":
            return "#ef4444"

        if self.variant == "warning":
            return "#f59e0b"

        return "#f9fafb"