from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
)


class PortfolioSummaryPanel(QFrame):
    """
    Live Desk portfolio summary panel.

    Presentation only.

    Displays already calculated dashboard values.
    Does not calculate portfolio statistics.
    """

    def __init__(self):
        super().__init__()

        self.setObjectName("PortfolioSummaryPanel")

        self.title_label = QLabel("Portfolio")
        self.title_label.setObjectName("PanelTitle")

        self.grid = QGridLayout()
        self.grid.setSpacing(12)

        self.value_labels: dict[str, QLabel] = {}

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addLayout(self.grid)

        self.setLayout(layout)

        self.set_values(
            cash=0.0,
            equity=0.0,
            open_profit_loss=0.0,
            closed_profit_loss=0.0,
            total_profit_loss=0.0,
            total_return_percent=0.0,
        )

    def set_values(
        self,
        cash: float,
        equity: float,
        open_profit_loss: float,
        closed_profit_loss: float,
        total_profit_loss: float,
        total_return_percent: float,
    ) -> None:
        values = {
            "Cash": f"€ {cash:.2f}",
            "Equity": f"€ {equity:.2f}",
            "Open P/L": f"€ {open_profit_loss:.2f}",
            "Closed P/L": f"€ {closed_profit_loss:.2f}",
            "Total P/L": f"€ {total_profit_loss:.2f}",
            "Return": f"{total_return_percent:.2f}%",
        }

        self._render_values(values)

    def _render_values(
        self,
        values: dict[str, str],
    ) -> None:
        self._clear_grid()

        self.value_labels = {}

        for index, (label, value) in enumerate(values.items()):
            row = index // 2
            column = (index % 2) * 2

            label_widget = QLabel(label)
            label_widget.setObjectName("MetricLabel")

            value_widget = QLabel(value)
            value_widget.setObjectName("MetricValue")

            self.value_labels[label] = value_widget

            self.grid.addWidget(label_widget, row, column)
            self.grid.addWidget(value_widget, row, column + 1)

    def _clear_grid(self) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.deleteLater()