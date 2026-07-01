from services.paper_trading.models import PaperAccount, PaperTradingResult, PaperTradeRecord
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.paper_trading_presenter import PaperTradingPresenter


def test_paper_trading_presenter_creates_core_sections():
    account = PaperAccount(starting_cash=10000.0)
    result = PaperTradingResult(
        operation="SUMMARY",
        account=account,
        cash_balance=10000.0,
        equity=10000.0,
        open_positions=0,
    )

    sections = PaperTradingPresenter().create_sections(result)

    assert [section.title for section in sections] == [
        "Paper Trading Account",
        "Open Paper Positions",
        "Paper Trade Execution",
    ]
    assert sections[0].metrics[0].value == "SUMMARY"
    assert sections[0].metrics[1].value == "Yes"
    assert sections[0].metrics[2].value == "10000.00"


def test_paper_trading_presenter_formats_execution_details():
    account = PaperAccount(starting_cash=10000.0)
    trade = PaperTradeRecord(
        symbol="AAPL",
        action="BUY",
        quantity=10,
        entry_price=150.0,
        status="OPEN",
        reason="TRADE_PLAN_EXECUTION",
    )
    result = PaperTradingResult(
        operation="EXECUTE",
        account=account,
        executed_trade=trade,
        cash_balance=8500.0,
        equity=10000.0,
    )

    execution = PaperTradingPresenter().create_sections(result)[2]

    assert [metric.value for metric in execution.metrics[:5]] == [
        "BUY",
        "OPEN",
        "AAPL",
        "10",
        "150.00",
    ]


def test_paper_trading_presenter_includes_diagnostics_when_available():
    account = PaperAccount(starting_cash=10000.0)
    result = PaperTradingResult(operation="EXECUTE", account=account, valid_operation=False)
    result.add_warning("Invalid paper trading operation.")
    result.add_reason("Paper trading validation completed.")

    sections = PaperTradingPresenter().create_sections(result)

    assert sections[-1].title == "Paper Trading Diagnostics"
    assert sections[-1].metrics[0].label == "Warning 1"
    assert sections[-1].metrics[0].value == "Invalid paper trading operation."
    assert sections[-1].metrics[1].label == "Reason 1"


def test_gui_shell_builds_paper_trading_dashboard_without_executing_trades():
    account = PaperAccount(starting_cash=10000.0)
    result = PaperTradingResult(
        operation="SUMMARY",
        account=account,
        cash_balance=9000.0,
        equity=10250.0,
        open_positions=1,
    )

    state = GuiShell().build_paper_trading_dashboard(result)

    assert state.current_page == GuiPage.PAPER_TRADING
    assert state.status_message == "Paper trading dashboard updated"
    assert state.sections[0].title == "Paper Trading Account"
    assert state.sections[0].metrics[3].value == "10250.00"
