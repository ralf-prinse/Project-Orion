from services.backtesting.models import BacktestResult, BacktestTrade
from ui.foundation.backtesting_presenter import BacktestingPresenter
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry


def make_result(**overrides):
    values = {
        "symbol": "AAPL",
        "valid_backtest": True,
        "total_trades": 1,
        "winning_trades": 1,
        "losing_trades": 0,
        "win_rate": 100.0,
        "total_gross_pnl": 100.0,
        "total_return_pct": 1.0,
        "max_drawdown": 0.0,
    }
    values.update(overrides)
    return BacktestResult(**values)


def test_backtesting_presenter_creates_core_sections():
    result = make_result()

    sections = BacktestingPresenter().create_sections(result)

    assert [section.title for section in sections] == [
        "Backtesting Dashboard",
        "Backtest Trade Statistics",
        "Backtest Trade Log",
    ]
    assert sections[0].metrics[0].value == "AAPL"
    assert sections[0].metrics[1].value == "Yes"
    assert sections[0].metrics[3].value == "100.00"
    assert sections[1].metrics[2].value == "100.00%"


def test_backtesting_presenter_formats_trade_log():
    result = make_result()
    result.add_trade(
        BacktestTrade(
            symbol="MSFT",
            action="BUY",
            entry_date="2026-01-01",
            entry_price=100.0,
            exit_date="2026-01-05",
            exit_price=110.0,
            shares=10,
            exit_reason="TARGET",
            gross_pnl=100.0,
            return_pct=10.0,
        )
    )

    sections = BacktestingPresenter().create_sections(result)
    trade_metric = sections[2].metrics[0]

    assert trade_metric.label == "Trade 1"
    assert "MSFT BUY" in trade_metric.value
    assert "100.00 → 110.00" in trade_metric.value
    assert trade_metric.helper_text == "Exit reason: TARGET"


def test_backtesting_presenter_adds_diagnostics_when_available():
    result = make_result(valid_backtest=False)
    result.add_warning("Entry price was not reached.")
    result.add_reason("Backtest skipped safely.")

    sections = BacktestingPresenter().create_sections(result)

    assert sections[-1].title == "Backtesting Diagnostics"
    assert sections[-1].metrics[0].label == "Warning 1"
    assert sections[-1].metrics[1].label == "Reason 1"


def test_gui_shell_builds_backtesting_dashboard():
    shell = GuiShell()
    result = make_result(symbol="NVDA")

    state = shell.build_backtesting_dashboard(result)

    assert state.current_page == GuiPage.BACKTESTING
    assert state.status_message == "Backtesting dashboard updated"
    assert state.sections[0].title == "Backtesting Dashboard"
    assert state.sections[0].metrics[0].value == "NVDA"


def test_navigation_registry_contains_backtesting_page():
    registry = NavigationRegistry()

    assert registry.contains_page(GuiPage.BACKTESTING) is True

    labels_by_page = {item.page: item.label for item in registry.get_items()}
    assert labels_by_page[GuiPage.BACKTESTING] == "Backtesting"
