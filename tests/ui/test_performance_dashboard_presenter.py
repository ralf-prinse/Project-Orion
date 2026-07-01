from services.performance.models import PerformanceResult
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.performance_dashboard_presenter import PerformanceDashboardPresenter


def test_performance_dashboard_presenter_creates_core_sections():
    presenter = PerformanceDashboardPresenter()
    result = PerformanceResult(label="Backtest", valid_analysis=True)

    sections = presenter.create_sections(result)

    assert [section.title for section in sections] == [
        "Performance Dashboard",
        "Trade Quality",
        "Risk & Drawdown",
    ]
    assert sections[0].metrics[0].value == "Backtest"
    assert sections[0].metrics[1].value == "Yes"


def test_performance_dashboard_presenter_formats_trade_quality_metrics():
    presenter = PerformanceDashboardPresenter()
    result = PerformanceResult(
        total_trades=20,
        winning_trades=12,
        losing_trades=7,
        breakeven_trades=1,
        win_rate=60.456,
        expectancy=32.789,
    )

    trade_quality = presenter.create_sections(result)[1]

    assert [metric.value for metric in trade_quality.metrics] == [
        "20",
        "12",
        "7",
        "1",
        "60.46%",
        "32.79",
    ]


def test_performance_dashboard_presenter_includes_diagnostics_when_available():
    presenter = PerformanceDashboardPresenter()
    result = PerformanceResult()
    result.add_warning("No trades available.")
    result.add_reason("Performance analytics completed.")

    sections = presenter.create_sections(result)

    assert sections[-1].title == "Performance Diagnostics"
    assert sections[-1].metrics[0].label == "Warning 1"
    assert sections[-1].metrics[0].value == "No trades available."
    assert sections[-1].metrics[1].label == "Reason 1"


def test_gui_shell_builds_performance_dashboard_without_calculating_metrics():
    shell = GuiShell()
    result = PerformanceResult(total_trades=5, net_pnl=250.0)

    state = shell.build_performance_dashboard(result)

    assert state.current_page == GuiPage.PERFORMANCE
    assert state.status_message == "Performance dashboard updated"
    assert state.sections[0].title == "Performance Dashboard"
    assert state.sections[0].metrics[2].value == "250.00"
