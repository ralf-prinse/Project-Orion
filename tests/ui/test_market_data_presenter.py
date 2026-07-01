from services.market_data.base_provider import MarketDataProviderStats, MarketQuote
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.market_data_presenter import MarketDataPresenter
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry


def _sample_quotes() -> list[MarketQuote]:
    return [
        MarketQuote(
            symbol="msft",
            price=420.125,
            volume=25000000,
            previous_close=418.5,
            change_percent=0.39,
        ),
        MarketQuote(
            symbol="aapl",
            price=195.5,
            volume=52000000,
            previous_close=193.0,
            change_percent=1.30,
        ),
    ]


def _sample_stats() -> MarketDataProviderStats:
    return MarketDataProviderStats(
        provider_name="FakeMarketDataProvider",
        requested_symbols=3,
        received_quotes=2,
        missing_quotes=0,
        duration_seconds=0.25,
    )


def test_market_data_presenter_creates_stable_sections():
    sections = MarketDataPresenter().create_sections(_sample_quotes(), _sample_stats())

    assert [section.title for section in sections] == [
        "Market Data Dashboard",
        "Quotes",
        "Quote Service Statistics",
    ]
    assert sections[0].metrics[0].value == "2"
    assert sections[0].metrics[1].value == "MSFT, AAPL"
    assert sections[0].metrics[2].value == "3"
    assert sections[1].metrics[0].label == "AAPL Price"
    assert sections[1].metrics[0].value == "$195.50"
    assert sections[1].metrics[1].value == "52,000,000"
    assert sections[1].metrics[3].value == "1.30%"
    assert sections[2].metrics[1].value == "FakeMarketDataProvider"


def test_market_data_presenter_handles_empty_quotes_and_missing_stats():
    sections = MarketDataPresenter().create_sections([], None)

    assert sections[0].metrics[0].value == "0"
    assert sections[0].metrics[1].value == "None"
    assert sections[0].metrics[2].value == "N/A"
    assert sections[1].metrics[0].value == "None"
    assert sections[2].metrics[0].value == "N/A"


def test_market_data_presenter_marks_optional_quote_values_as_na():
    sections = MarketDataPresenter().create_sections([MarketQuote("NVDA", 900.0, 1000)])

    assert sections[1].metrics[0].value == "$900.00"
    assert sections[1].metrics[2].value == "N/A"
    assert sections[1].metrics[3].value == "N/A"


def test_gui_shell_builds_market_data_dashboard_without_fetching_quotes():
    state = GuiShell().build_market_data_dashboard(_sample_quotes(), _sample_stats())

    assert state.current_page == GuiPage.MARKET_DATA
    assert state.status_message == "Market data dashboard updated"
    assert state.sections[0].title == "Market Data Dashboard"
    assert state.sections[1].title == "Quotes"


def test_dashboard_composer_can_include_market_data():
    sections = DashboardComposer().compose(
        market_quotes=_sample_quotes(),
        quote_stats=_sample_stats(),
    )

    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "Market Data"
    assert sections[0].metrics[1].value == "1"
    assert sections[1].title == "Market Data Dashboard"


def test_navigation_registry_contains_market_data_page_after_dashboard():
    items = NavigationRegistry().get_items()
    pages = [item.page for item in items]
    labels_by_page = {item.page: item.label for item in items}

    assert GuiPage.MARKET_DATA in pages
    assert labels_by_page[GuiPage.MARKET_DATA] == "Market Data"
    assert pages.index(GuiPage.DASHBOARD) < pages.index(GuiPage.MARKET_DATA)
    assert pages.index(GuiPage.MARKET_DATA) < pages.index(GuiPage.DECISIONS)
