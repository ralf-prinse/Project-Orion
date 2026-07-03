from ui.foundation.chart_models import GuiChartType
from ui.foundation.dashboard_workspace_presenter import DashboardWorkspacePresenter
from ui.foundation.equity_curve_chart_presenter import EquityCurveChartPresenter


class DummyDashboardPresenter:
    def create_cards(self, dashboard_data):
        return []


def test_dashboard_workspace_presenter_includes_equity_curve_chart():
    presenter = DashboardWorkspacePresenter(
        dashboard_presenter=DummyDashboardPresenter(),
        equity_curve_presenter=EquityCurveChartPresenter(),
    )

    workspace = presenter.create_workspace({})

    assert len(workspace.charts) == 1

    chart = workspace.charts[0]

    assert chart.title == "Equity Curve"
    assert chart.chart_type == GuiChartType.LINE
    assert chart.metadata["widget"] == "equity_curve"