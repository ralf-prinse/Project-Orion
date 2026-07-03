from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget


class ChartContainer(QWidget):
    """
    Presentation-only chart container.

    Owns layout placement for chart widgets inside a workspace.

    No business logic.
    No calculations.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(22)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

        self.widgets: list[QWidget] = []

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.widgets.clear()

    def add_chart_widget(self, widget: QWidget):
        self.widgets.append(widget)
        self.layout.addWidget(widget)

    def add_chart_widgets(self, widgets: list[QWidget]):
        for widget in widgets:
            self.add_chart_widget(widget)