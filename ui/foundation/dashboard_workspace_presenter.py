from __future__ import annotations

from ui.foundation.dashboard_2_presenter import Dashboard2Presenter
from ui.foundation.dashboard_data import DashboardData
from ui.foundation.workspace import GuiWorkspace


class DashboardWorkspacePresenter:
    """
    Unified dashboard workspace presenter.

    Produces one GuiWorkspace from existing Dashboard 2.0 presentation cards.
    Presentation orchestration only.
    """

    def __init__(
        self,
        dashboard_presenter: Dashboard2Presenter | None = None,
    ) -> None:
        self._dashboard_presenter = (
            dashboard_presenter
            if dashboard_presenter is not None
            else Dashboard2Presenter()
        )

    def create_workspace(
        self,
        data: DashboardData | None = None,
    ) -> GuiWorkspace:
        cards = self._dashboard_presenter.create_cards(data)

        return GuiWorkspace(
            title="Dashboard",
            subtitle="Unified Dashboard Workspace",
            cards=cards,
            charts=[],
            sections=[],
            status="ready",
            metadata={
                "version": "4.3",
                "pipeline": "GuiWorkspace",
            },
        )

    def create_default_workspace(self) -> GuiWorkspace:
        return self.create_workspace(DashboardData())