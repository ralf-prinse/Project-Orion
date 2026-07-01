from services.performance.models import PerformanceResult
from ui.foundation.dashboard_presenter import DashboardPresenter
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage


def test_dashboard_presenter_creates_system_overview_without_performance_result():
    presenter = DashboardPresenter()

    sections = presenter.create_overview_sections(total_open_positions=2, total_watchlist_items=15)

    assert len(sections) == 1
    assert sections[0].title == "System Overview"
    assert sections[0].metrics[0].value == "2"
    assert sections[0].metrics[1].value == "15"


def test_dashboard_presenter_adds_performance_snapshot_when_available():
    presenter = DashboardPresenter()
    result = PerformanceResult(
        total_trades=12,
        win_rate=58.3333,
        net_pnl=1240.5,
        max_drawdown_pct=7.891,
    )

    sections = presenter.create_overview_sections(performance_result=result)

    assert len(sections) == 2
    assert sections[1].title == "Performance Snapshot"
    assert [metric.value for metric in sections[1].metrics] == ["12", "58.33%", "1240.50", "7.89%"]


def test_gui_shell_build_dashboard_updates_dashboard_state():
    shell = GuiShell()

    state = shell.build_dashboard(total_open_positions=1, total_watchlist_items=4)

    assert state.current_page == GuiPage.DASHBOARD
    assert state.status_message == "Dashboard updated"
    assert state.sections[0].metrics[0].value == "1"
