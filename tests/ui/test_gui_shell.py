import pytest

from services.portfolio.models import PortfolioPosition, PortfolioState
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiApplicationConfig, GuiNavigationItem, GuiPage, GuiMetric, GuiSection
from ui.foundation.navigation import NavigationRegistry


def test_gui_shell_initializes_with_default_navigation():
    shell = GuiShell()

    assert shell.state.current_page == GuiPage.DASHBOARD
    assert len(shell.state.navigation_items) == 10
    assert shell.state.status_message == "Ready"


def test_gui_shell_can_navigate_to_registered_page():
    shell = GuiShell()

    state = shell.navigate_to(GuiPage.PERFORMANCE)

    assert state.current_page == GuiPage.PERFORMANCE
    assert state.status_message == "Current page: performance"


def test_gui_shell_rejects_unknown_page_for_custom_navigation():
    shell = GuiShell(
        navigation_registry=NavigationRegistry(
            items=[GuiNavigationItem(GuiPage.DASHBOARD, "Dashboard", 10)]
        )
    )

    with pytest.raises(ValueError):
        shell.navigate_to(GuiPage.PERFORMANCE)


def test_gui_shell_falls_back_when_config_default_page_is_not_registered():
    shell = GuiShell(
        config=GuiApplicationConfig(default_page=GuiPage.PERFORMANCE),
        navigation_registry=NavigationRegistry(
            items=[GuiNavigationItem(GuiPage.SCANNER, "Scanner", 10)]
        ),
    )

    assert shell.state.current_page == GuiPage.SCANNER


def test_gui_shell_sets_sections_without_calculating_trading_logic():
    shell = GuiShell()
    sections = [GuiSection("Example", [GuiMetric("Metric", "Value")])]

    state = shell.set_sections(sections)

    assert state.sections == sections

from types import SimpleNamespace


def test_gui_shell_builds_scanner_dashboard_without_scanning():
    shell = GuiShell()
    scanner_result = SimpleNamespace(
        opportunities=[SimpleNamespace(symbol="MSFT", action="HOLD", confidence=72.0, reason="Watchlist candidate")],
        status=SimpleNamespace(universe_count=20, quotes_count=18, opportunities_count=1, messages=[]),
    )

    state = shell.build_scanner_dashboard(scanner_result)

    assert state.current_page == GuiPage.SCANNER
    assert state.status_message == "Scanner dashboard updated"
    assert state.sections[0].title == "Scanner Summary"
    assert state.sections[3].metrics[0].value == "MSFT"


def test_gui_shell_unified_dashboard_accepts_scanner_result():
    shell = GuiShell()
    scanner_result = SimpleNamespace(
        opportunities=[],
        status=SimpleNamespace(universe_count=0, messages=["Geen symbolen ontvangen."]),
    )

    state = shell.build_unified_dashboard(scanner_result=scanner_result)

    assert state.current_page == GuiPage.DASHBOARD
    assert state.sections[0].metrics[0].value == "Scanner"
    assert any(section.title == "Scanner Diagnostics" for section in state.sections)


def test_gui_shell_builds_portfolio_dashboard_without_portfolio_logic():
    shell = GuiShell()
    portfolio_state = PortfolioState(
        cash=3000.0,
        positions={
            "AAPL": PortfolioPosition(
                symbol="AAPL",
                quantity=2,
                average_price=150.0,
                current_price=160.0,
            )
        },
    )

    state = shell.build_portfolio_dashboard(portfolio_state=portfolio_state)

    assert state.current_page == GuiPage.PORTFOLIO
    assert state.status_message == "Portfolio dashboard updated"
    assert state.sections[0].title == "Portfolio Account"
    assert state.sections[1].title == "Open Positions"
