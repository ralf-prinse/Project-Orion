from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class PortfolioWorkspace(BaseWorkspace):
    """
    Presentation-only portfolio workspace.

    This workspace displays deterministic portfolio information produced by
    Orion services. It never performs portfolio calculations itself.
    """

    def __init__(self, theme):
        super().__init__(
            theme=theme,
            title="Portfolio",
            intro="Bekijk de huidige portefeuille, allocatie en risico-overzicht.",
        )

        self.overview_panel = WorkspacePanel(
            theme=self.theme,
            title="Portfolio Overview",
            body="Nog geen portefeuillegegevens beschikbaar.",
        )

        self.positions_panel = WorkspacePanel(
            theme=self.theme,
            title="Open Positions",
            body="Er zijn momenteel geen open posities.",
        )

        self.exposure_panel = WorkspacePanel(
            theme=self.theme,
            title="Exposure",
            body="Exposure-overzicht wordt later gekoppeld.",
        )

        self._build_layout()

    def _build_layout(self):
        self.add_workspace_widget(self.overview_panel)
        self.add_workspace_widget(self.positions_panel)
        self.add_workspace_widget(self.exposure_panel)

    def set_overview(self, text: str):
        self.overview_panel.set_body(text)

    def set_positions(self, text: str):
        self.positions_panel.set_body(text)

    def set_exposure(self, text: str):
        self.exposure_panel.set_body(text)

    def clear(self):
        self.overview_panel.set_body(
            "Nog geen portefeuillegegevens beschikbaar."
        )
        self.positions_panel.set_body(
            "Er zijn momenteel geen open posities."
        )
        self.exposure_panel.set_body(
            "Exposure-overzicht wordt later gekoppeld."
        )