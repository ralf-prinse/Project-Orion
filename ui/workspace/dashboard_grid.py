from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QWidget

from ui.foundation.dashboard_widget_factory import DashboardWidgetFactory
from ui.foundation.models import GuiMetricCard
from ui.foundation.workspace import GuiWorkspacePanel


class DashboardGrid(QWidget):
    """
    Responsive presentation grid.

    Supports:
        - Metric cards
        - Workspace panels

    Widget creation is delegated to DashboardWidgetFactory.

    Presentation only.
    """

    opportunity_selected = Signal(str)

    def __init__(self, theme):
        super().__init__()

        self.theme = theme

        self.layout = QGridLayout()
        self.layout.setSpacing(22)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

        self.widgets: list[QWidget] = []

    def clear(self) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.widgets.clear()

    # ------------------------------------------------------------------
    # Metric Cards
    # ------------------------------------------------------------------

    def add_card(self, card: GuiMetricCard) -> None:
        widget = DashboardWidgetFactory.create(
            theme=self.theme,
            card=card,
        )

        self._add_widget(widget, card.column_span)

    def add_cards(self, cards: list[GuiMetricCard]) -> None:
        for card in cards:
            self.add_card(card)

    # ------------------------------------------------------------------
    # Workspace Panels
    # ------------------------------------------------------------------

    def add_panel(self, panel: GuiWorkspacePanel) -> None:
        widget = DashboardWidgetFactory.create_panel(
            theme=self.theme,
            panel=panel,
        )

        self._connect_panel_signals(widget)

        self._add_widget(widget, 3)

    def add_panels(self, panels: list[GuiWorkspacePanel]) -> None:
        for panel in panels:
            self.add_panel(panel)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _connect_panel_signals(self, widget: QWidget) -> None:
        opportunity_signal = getattr(widget, "opportunity_selected", None)

        if opportunity_signal is None:
            return

        opportunity_signal.connect(self.opportunity_selected.emit)

    def _add_widget(
        self,
        widget: QWidget,
        column_span: int = 1,
    ) -> None:
        self.widgets.append(widget)

        index = len(self.widgets) - 1

        columns = 3

        row = index // columns
        column = index % columns

        span = max(1, min(column_span, columns))

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