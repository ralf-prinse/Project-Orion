from __future__ import annotations

from ui.foundation.dashboard_2_presenter import Dashboard2Presenter
from ui.foundation.dashboard_data import DashboardData
from ui.foundation.equity_curve_chart_presenter import EquityCurveChartPresenter
from ui.foundation.workspace import GuiWorkspace


class DashboardWorkspacePresenter:
    """
    Unified dashboard workspace presenter.

    Produces one GuiWorkspace from existing Dashboard 2.0 presentation cards
    and reusable dashboard chart presenters.

    Presentation orchestration only.
    """

    def __init__(
        self,
        dashboard_presenter: Dashboard2Presenter | None = None,
        equity_curve_presenter: EquityCurveChartPresenter | None = None,
    ) -> None:
        self._dashboard_presenter = (
            dashboard_presenter
            if dashboard_presenter is not None
            else Dashboard2Presenter()
        )

        self._equity_curve_presenter = (
            equity_curve_presenter
            if equity_curve_presenter is not None
            else EquityCurveChartPresenter()
        )

    def create_workspace(
        self,
        data: DashboardData | None = None,
    ) -> GuiWorkspace:
        cards = self._dashboard_presenter.create_cards(data)
        charts = [
            self._equity_curve_presenter.present()
        ]

        return GuiWorkspace(
            title="Dashboard",
            subtitle="Unified Dashboard Workspace",
            cards=cards,
            charts=charts,
            chart_sections=[],
            sections=[],
            status="ready",
            metadata={
                "version": "4.3",
                "pipeline": "GuiWorkspace",
            },
        )

    def create_default_workspace(self) -> GuiWorkspace:
        return self.create_workspace(DashboardData())