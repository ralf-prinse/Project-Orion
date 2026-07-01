import pytest

from ui.components import (
    BadgeStatus,
    CardComponent,
    MetricTileComponent,
    PanelComponent,
    SectionHeaderComponent,
    SidebarComponent,
    StatusBadgeComponent,
)
from ui.foundation.models import GuiMetric, GuiNavigationItem, GuiPage


def test_card_component_creates_display_only_card_model():
    component = CardComponent()
    metric = GuiMetric("Signals", "12")

    card = component.create("Scanner", "Latest opportunities", [metric], accent="Primary")

    assert card.title == "Scanner"
    assert card.description == "Latest opportunities"
    assert card.metrics == [metric]
    assert card.accent == "primary"
    assert "background-color" in component.stylesheet()


def test_metric_tile_component_normalizes_values():
    tile = MetricTileComponent().create("Buy", 26, "Top setups", trend="Positive")

    assert tile.label == "Buy"
    assert tile.value == "26"
    assert tile.helper_text == "Top setups"
    assert tile.trend == "positive"


def test_status_badge_component_maps_status_to_theme_colour():
    badge = StatusBadgeComponent().create("Scanning", BadgeStatus.RUNNING)

    assert badge.label == "SCANNING"
    assert badge.status == BadgeStatus.RUNNING
    assert badge.color


def test_status_badge_rejects_unknown_status():
    with pytest.raises(ValueError):
        StatusBadgeComponent().create("Unknown", "not-a-status")


def test_section_header_component_creates_header_model():
    header = SectionHeaderComponent().create("Dashboard", "Market overview", "Refresh")

    assert header.title == "Dashboard"
    assert header.subtitle == "Market overview"
    assert header.action_label == "Refresh"


def test_sidebar_component_adds_icons_and_selected_state():
    items = [
        GuiNavigationItem(GuiPage.DASHBOARD, "Dashboard", 10),
        GuiNavigationItem(GuiPage.PORTFOLIO, "Portfolio", 20),
    ]

    buttons = SidebarComponent().create_buttons(items, current_page=GuiPage.PORTFOLIO)

    assert buttons[0].label == "Dashboard"
    assert buttons[0].selected is False
    assert buttons[1].label == "Portfolio"
    assert buttons[1].selected is True
    assert buttons[1].icon


def test_panel_component_groups_cards_without_business_logic():
    card = CardComponent().create("Performance")

    panel = PanelComponent().create("Dashboard", [card], "Overview")

    assert panel.title == "Dashboard"
    assert panel.cards == [card]
    assert panel.description == "Overview"
