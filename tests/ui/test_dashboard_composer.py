from services.ai.models import AIExplanationResult
from services.paper_trading.models import PaperAccount, PaperTradingResult
from services.performance.models import PerformanceResult
from services.portfolio.models import PortfolioPosition, PortfolioResult, PortfolioState
from services.planner.models import TradePlanResult
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage


def test_dashboard_composer_returns_summary_when_no_results_are_available():
    composer = DashboardComposer()

    sections = composer.compose()

    assert len(sections) == 1
    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "None"
    assert sections[0].metrics[1].value == "0"


def test_dashboard_composer_combines_available_presenters_deterministically():
    performance = PerformanceResult(label="Backtest", valid_analysis=True, total_trades=3)
    trade_plan = TradePlanResult(
        symbol="AAPL",
        action="BUY",
        valid_plan=True,
        entry_price=100.0,
        stop_loss=95.0,
        target_price=110.0,
        shares=10,
    )

    sections = DashboardComposer().compose(
        performance_result=performance,
        trade_plan_result=trade_plan,
    )

    titles = [section.title for section in sections]

    assert titles[0] == "Unified Dashboard Summary"
    assert "Performance Dashboard" in titles
    assert "Trade Plan Summary" in titles
    assert "Paper Trading Account" not in titles


def test_dashboard_composer_can_include_paper_trading_and_explanation_sections():
    account = PaperAccount(starting_cash=10000.0)
    paper_result = PaperTradingResult(
        operation="STATUS",
        account=account,
        cash_balance=10000.0,
        equity=10000.0,
    )
    explanation = AIExplanationResult(
        symbol="MSFT",
        valid_explanation=True,
        summary="Deterministic explanation summary.",
        source_count=1,
    )

    sections = DashboardComposer().compose(
        paper_trading_result=paper_result,
        explanation_result=explanation,
    )

    titles = [section.title for section in sections]

    assert "Paper Trading Account" in titles
    assert "AI Explanation Summary" in titles
    assert sections[0].metrics[1].value == "2"


def test_gui_shell_builds_unified_dashboard_without_changing_engine_outputs():
    shell = GuiShell()
    performance = PerformanceResult(label="Paper Trading", total_trades=5)

    state = shell.build_unified_dashboard(performance_result=performance)

    assert state.current_page == GuiPage.DASHBOARD
    assert state.status_message == "Unified dashboard updated"
    assert state.sections[0].title == "Unified Dashboard Summary"
    assert any(section.title == "Performance Dashboard" for section in state.sections)

from types import SimpleNamespace


def test_dashboard_composer_can_include_scanner_sections():
    scanner_result = SimpleNamespace(
        opportunities=[SimpleNamespace(symbol="NVDA", action="BUY", confidence=91.0, reason="High quality setup")],
        status=SimpleNamespace(
            universe_count=500,
            quotes_count=450,
            technical_results_count=25,
            opportunities_count=1,
            messages=[],
        ),
    )

    sections = DashboardComposer().compose(scanner_result=scanner_result)
    titles = [section.title for section in sections]

    assert sections[0].metrics[0].value == "Scanner"
    assert sections[0].metrics[1].value == "1"
    assert "Scanner Summary" in titles
    assert "Top Opportunities" in titles


def test_dashboard_composer_can_include_portfolio_sections():
    portfolio_state = PortfolioState(
        cash=7500.0,
        positions={
            "AAPL": PortfolioPosition(
                symbol="AAPL",
                quantity=4,
                average_price=180.0,
                current_price=190.0,
            )
        },
    )
    portfolio_result = PortfolioResult(
        symbol="AAPL",
        portfolio_allowed=True,
        proposed_position_value=760.0,
    )

    sections = DashboardComposer().compose(
        portfolio_state=portfolio_state,
        portfolio_result=portfolio_result,
    )
    titles = [section.title for section in sections]

    assert sections[0].metrics[0].value == "Portfolio"
    assert sections[0].metrics[1].value == "1"
    assert "Portfolio Account" in titles
    assert "Open Positions" in titles
    assert "Portfolio Validation" in titles

from services.backtesting.models import BacktestResult


def test_dashboard_composer_can_include_backtesting_sections():
    backtest = BacktestResult(
        symbol="AAPL",
        valid_backtest=True,
        total_trades=1,
        winning_trades=1,
        win_rate=100.0,
        total_gross_pnl=100.0,
        total_return_pct=1.0,
    )

    sections = DashboardComposer().compose(backtest_result=backtest)
    titles = [section.title for section in sections]

    assert sections[0].metrics[0].value == "Backtesting"
    assert sections[0].metrics[1].value == "1"
    assert "Backtesting Dashboard" in titles
    assert "Backtest Trade Statistics" in titles
