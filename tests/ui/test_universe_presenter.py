from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.universe_presenter import UniversePresenter


def _sample_symbols() -> list[str]:
    return ["aapl", "MSFT", "nvda", "tsla"]


def _sample_update_stats() -> dict[str, int]:
    return {
        "nasdaq": 2500,
        "us_other": 3700,
        "us_market": 6200,
    }


def test_universe_presenter_creates_stable_sections():
    sections = UniversePresenter().create_sections(_sample_symbols(), _sample_update_stats())

    assert [section.title for section in sections] == [
        "Universe Dashboard",
        "Universe Symbols",
        "Universe Update Statistics",
    ]
    assert sections[0].metrics[0].value == "4"
    assert sections[0].metrics[1].value == "AAPL"
    assert sections[0].metrics[2].value == "6200"
    assert sections[1].metrics[0].value == "4"
    assert sections[1].metrics[1].value == "AAPL, MSFT, NVDA, TSLA"
    assert sections[2].metrics[0].value == "2500"
    assert sections[2].metrics[1].value == "3700"
    assert sections[2].metrics[2].value == "6200"


def test_universe_presenter_handles_empty_symbols_and_missing_stats():
    sections = UniversePresenter().create_sections([], None)

    assert sections[0].metrics[0].value == "0"
    assert sections[0].metrics[1].value == "N/A"
    assert sections[0].metrics[2].value == "N/A"
    assert sections[1].metrics[0].value == "None"
    assert sections[2].metrics[0].value == "N/A"


def test_gui_shell_builds_universe_dashboard_without_loading_or_downloading_universe():
    state = GuiShell().build_universe_dashboard(_sample_symbols(), _sample_update_stats())

    assert state.current_page == GuiPage.UNIVERSE
    assert state.status_message == "Universe dashboard updated"
    assert state.sections[0].title == "Universe Dashboard"
    assert state.sections[1].title == "Universe Symbols"


def test_dashboard_composer_can_include_universe_output():
    sections = DashboardComposer().compose(
        universe_symbols=_sample_symbols(),
        universe_update_stats=_sample_update_stats(),
    )

    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "Universe"
    assert sections[0].metrics[1].value == "1"
    assert sections[1].title == "Universe Dashboard"


def test_navigation_registry_contains_universe_page_before_market_data():
    items = NavigationRegistry().get_items()
    pages = [item.page for item in items]
    labels_by_page = {item.page: item.label for item in items}

    assert GuiPage.UNIVERSE in pages
    assert labels_by_page[GuiPage.UNIVERSE] == "Universe"
    assert pages.index(GuiPage.DASHBOARD) < pages.index(GuiPage.UNIVERSE)
    assert pages.index(GuiPage.UNIVERSE) < pages.index(GuiPage.MARKET_DATA)


def test_unified_dashboard_orders_universe_before_market_data():
    sections = DashboardComposer().compose(
        universe_symbols=["AAPL"],
        market_quotes=[],
    )

    assert sections[0].metrics[0].value == "Universe, Market Data"
    assert sections[1].title == "Universe Dashboard"
    assert sections[4].title == "Market Data Dashboard"
