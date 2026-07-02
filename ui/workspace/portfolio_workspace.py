from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ui.foundation.models import GuiSection, GuiWorkspace
from ui.widgets.chart_widget import ChartWidget
from ui.widgets.metric_card import MetricCard
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class PortfolioWorkspace(BaseWorkspace):
    """
    Professional Portfolio Dashboard Workspace.

    UX goals:
    - clear hierarchy (KPI → Charts → Sections)
    - balanced chart layout
    - readable spacing
    - production-grade layout structure
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Portfolio",
            intro="Bekijk de huidige portefeuille, allocatie en risico-overzicht.",
        )

        self._cards: list[MetricCard] = []
        self._charts: list[ChartWidget] = []
        self._panels: list[WorkspacePanel] = []

        self._card_row: QWidget | None = None
        self._chart_row: QWidget | None = None

    def set_workspace(self, workspace: GuiWorkspace):
        self._clear_rendered_content()

        if workspace.cards:
            self._card_row = self._create_card_row(workspace)
            self.add_workspace_widget(self._card_row)

        if workspace.charts:
            self._chart_row = self._create_chart_row(workspace)
            self.add_workspace_widget(self._chart_row)

        self.set_sections(workspace.sections)

    def set_sections(self, sections: list[GuiSection]):
        for panel in self._panels:
            panel.setParent(None)

        self._panels.clear()

        for section in sections:
            panel = WorkspacePanel.from_section(
                theme=self.theme,
                section=section,
            )

            self._panels.append(panel)
            self.add_workspace_widget(panel)

    def clear(self):
        self._clear_rendered_content()

    # -----------------------------
    # KPI LAYER
    # -----------------------------
    def _create_card_row(self, workspace: GuiWorkspace) -> QWidget:
        row = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(14)

        for card in workspace.cards:
            widget = MetricCard(
                theme=self.theme,
                card=card,
            )
            self._cards.append(widget)
            layout.addWidget(widget)

        row.setLayout(layout)
        return row

    # -----------------------------
    # CHART LAYER (UX IMPROVED)
    # -----------------------------
    def _create_chart_row(self, workspace: GuiWorkspace) -> QWidget:
        row = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 18)
        layout.setSpacing(16)

        # UX improvement: charts equal height & balanced width
        for chart in workspace.charts:
            widget = ChartWidget(
                theme=self.theme,
                chart=chart,
            )

            widget.setMinimumHeight(340)
            widget.setMaximumHeight(380)

            self._charts.append(widget)
            layout.addWidget(widget)

        row.setLayout(layout)
        return row

    def _clear_rendered_content(self):
        if self._card_row:
            self._card_row.setParent(None)
            self._card_row = None

        if self._chart_row:
            self._chart_row.setParent(None)
            self._chart_row = None

        for card in self._cards:
            card.setParent(None)
        self._cards.clear()

        for chart in self._charts:
            chart.setParent(None)
        self._charts.clear()

        for panel in self._panels:
            panel.setParent(None)
        self._panels.clear()