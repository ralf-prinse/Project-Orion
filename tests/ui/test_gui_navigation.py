import pytest

from ui.foundation.models import GuiNavigationItem, GuiPage
from ui.foundation.navigation import NavigationRegistry


def test_navigation_registry_returns_items_in_deterministic_order():
    registry = NavigationRegistry(
        items=[
            GuiNavigationItem(GuiPage.SETTINGS, "Settings", 30),
            GuiNavigationItem(GuiPage.DASHBOARD, "Dashboard", 10),
            GuiNavigationItem(GuiPage.PERFORMANCE, "Performance", 20),
        ]
    )

    pages = [item.page for item in registry.get_items()]

    assert pages == [GuiPage.DASHBOARD, GuiPage.PERFORMANCE, GuiPage.SETTINGS]


def test_navigation_registry_contains_known_page():
    registry = NavigationRegistry()

    assert registry.contains_page(GuiPage.DASHBOARD) is True
    assert registry.contains_page(GuiPage.PAPER_TRADING) is True


def test_navigation_registry_default_page_uses_first_ordered_item():
    registry = NavigationRegistry(
        items=[
            GuiNavigationItem(GuiPage.PERFORMANCE, "Performance", 20),
            GuiNavigationItem(GuiPage.SCANNER, "Scanner", 10),
        ]
    )

    assert registry.get_default_page() == GuiPage.SCANNER
