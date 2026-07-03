from ui.foundation.chart_models import GuiChartType
from ui.foundation.dashboard_workspace_presenter import DashboardWorkspacePresenter
from ui.foundation.workspace import GuiWorkspace


class DummyDashboardPresenter:
    def create_cards(self, dashboard_data):
        return [
            {
                "title": "Portfolio Value",
                "value": "€100,000",
            },
            {
                "title": "Open Positions",
                "value": "5",
            },
        ]


def test_dashboard_workspace_presenter_returns_workspace():
    presenter = DashboardWorkspacePresenter(
        dashboard_presenter=DummyDashboardPresenter()
    )

    workspace = presenter.create_workspace({})

    assert isinstance(workspace, GuiWorkspace)
    assert workspace.title == "Dashboard"
    assert workspace.status == "ready"

    assert len(workspace.cards) == 2
    assert len(workspace.charts) == 1
    assert workspace.charts[0].title == "Equity Curve"
    assert workspace.charts[0].chart_type == GuiChartType.LINE

    assert workspace.sections == []
    assert workspace.metadata["pipeline"] == "GuiWorkspace"
    assert workspace.metadata["version"] == "4.3"