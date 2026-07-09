from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class MetricTile(QFrame):
    """
    Reusable Live Desk metric tile.

    Presentation only.

    Displays a label, value and optional helper text.
    Does not calculate metrics.
    """

    def __init__(
        self,
        label: str,
        value: str = "-",
        helper_text: str = "",
    ):
        super().__init__()

        self.setObjectName("MetricTile")

        self.label_widget = QLabel(label)
        self.label_widget.setObjectName("MetricTileLabel")

        self.value_widget = QLabel(value)
        self.value_widget.setObjectName("MetricTileValue")

        self.helper_widget = QLabel(helper_text)
        self.helper_widget.setObjectName("MetricTileHelper")
        self.helper_widget.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label_widget)
        layout.addWidget(self.value_widget)

        if helper_text:
            layout.addWidget(self.helper_widget)

        self.setLayout(layout)

    def set_value(
        self,
        value: str,
        helper_text: str = "",
    ) -> None:
        self.value_widget.setText(value)
        self.helper_widget.setText(helper_text)

        if helper_text and self.helper_widget.parent() is None:
            self.layout().addWidget(self.helper_widget)