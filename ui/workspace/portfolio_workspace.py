from PySide6.QtWidgets import QHBoxLayout, QWidget

from ui.foundation.models import GuiSection, GuiWorkspace
from ui.widgets.metric_card import MetricCard
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class PortfolioWorkspace(BaseWorkspace):
    """
    Presentation-only portfolio workspace.

    This workspace displays the complete GuiWorkspace produced by portfolio
    workspace presenters. It owns layout only and performs no calculations.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Portfolio",
            intro="Bekijk de huidige portefeuille, allocatie en risico-overzicht.",
        )

        self._cards: list[MetricCard] = []
        self._panels: list[WorkspacePanel] = []
        self._card_row: QWidget | None = None

    def set_workspace(self, workspace: GuiWorkspace):
        """
        Render the complete portfolio workspace model.
        """

        self._clear_rendered_content()

        if workspace.cards:
            self._card_row = self._create_card_row(workspace)
            self.add_workspace_widget(self._card_row)

        self.set_sections(workspace.sections)

    def set_sections(self, sections: list[GuiSection]):
        """
        Render section panels.

        This method is retained for compatibility with existing callers.
        Prefer set_workspace() when rendering complete workspace models.
        """

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

    def _create_card_row(self, workspace: GuiWorkspace) -> QWidget:
        row = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(12)

        for card in workspace.cards:
            widget = MetricCard(
                theme=self.theme,
                card=card,
            )
            self._cards.append(widget)
            layout.addWidget(widget)

        row.setLayout(layout)
        return row

    def _clear_rendered_content(self):
        if self._card_row is not None:
            self._card_row.setParent(None)
            self._card_row = None

        for card in self._cards:
            card.setParent(None)

        self._cards.clear()

        for panel in self._panels:
            panel.setParent(None)

        self._panels.clear()