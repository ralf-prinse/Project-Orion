import pytest

from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiApplicationConfig, GuiNavigationItem, GuiPage, GuiMetric, GuiSection
from ui.foundation.navigation import NavigationRegistry


def test_gui_shell_initializes_with_default_navigation():
    shell = GuiShell()

    assert shell.state.current_page == GuiPage.DASHBOARD
    assert len(shell.state.navigation_items) == 7
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
