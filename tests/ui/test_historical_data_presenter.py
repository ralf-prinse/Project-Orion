import pandas as pd

from services.market_data.historical_provider import HistoricalProviderStats
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.historical_data_presenter import HistoricalDataPresenter
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry


def _sample_histories() -> dict[str, pd.DataFrame]:
    return {
        "msft": pd.DataFrame(
            {
                "Open": [410.0, 415.0],
                "High": [420.0, 422.0],
                "Low": [409.0, 414.0],
                "Close": [418.5, 420.125],
                "Volume": [24000000, 25000000],
            }
        ),
        "aapl": pd.DataFrame(
            {
                "Open": [190.0, 193.0, 194.0],
                "High": [195.0, 196.0, 197.0],
                "Low": [189.0, 192.0, 193.0],
                "Close": [193.0, 194.5, 195.5],
                "Volume": [50000000, 51000000, 52000000],
            }
        ),
    }


def _sample_stats() -> HistoricalProviderStats:
    return HistoricalProviderStats(
        provider_name="FakeHistoricalProvider",
        requested_symbols=3,
        received_symbols=2,
        missing_symbols=1,
        cache_hits=1,
        fresh_downloads=1,
        duration_seconds=0.75,
    )


def test_historical_data_presenter_creates_stable_sections():
    sections = HistoricalDataPresenter().create_sections(_sample_histories(), _sample_stats())

    assert [section.title for section in sections] == [
        "Historical Data Dashboard",
        "Historical Datasets",
        "Historical Provider Statistics",
    ]
    assert sections[0].metrics[0].value == "2"
    assert sections[0].metrics[1].value == "MSFT, AAPL"
    assert sections[0].metrics[2].value == "3"
    assert sections[1].metrics[0].label == "AAPL Candles"
    assert sections[1].metrics[0].value == "3"
    assert sections[1].metrics[1].value == "$195.50"
    assert sections[1].metrics[2].value == "52,000,000"
    assert sections[2].metrics[0].value == "FakeHistoricalProvider"
    assert sections[2].metrics[4].value == "1"


def test_historical_data_presenter_handles_empty_histories_and_missing_stats():
    sections = HistoricalDataPresenter().create_sections({}, None)

    assert sections[0].metrics[0].value == "0"
    assert sections[0].metrics[1].value == "None"
    assert sections[0].metrics[2].value == "N/A"
    assert sections[1].metrics[0].value == "None"
    assert sections[2].metrics[0].value == "N/A"


def test_historical_data_presenter_marks_missing_columns_as_na():
    histories = {"NVDA": pd.DataFrame({"Open": [900.0, 910.0]})}

    sections = HistoricalDataPresenter().create_sections(histories)

    assert sections[1].metrics[0].value == "2"
    assert sections[1].metrics[1].value == "N/A"
    assert sections[1].metrics[2].value == "N/A"


def test_gui_shell_builds_historical_data_dashboard_without_fetching_candles():
    state = GuiShell().build_historical_data_dashboard(_sample_histories(), _sample_stats())

    assert state.current_page == GuiPage.HISTORICAL_DATA
    assert state.status_message == "Historical data dashboard updated"
    assert state.sections[0].title == "Historical Data Dashboard"
    assert state.sections[1].title == "Historical Datasets"


def test_dashboard_composer_can_include_historical_data():
    sections = DashboardComposer().compose(
        historical_data=_sample_histories(),
        historical_stats=_sample_stats(),
    )

    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "Historical Data"
    assert sections[0].metrics[1].value == "1"
    assert sections[1].title == "Historical Data Dashboard"


def test_navigation_registry_contains_historical_data_page_after_market_data():
    items = NavigationRegistry().get_items()
    pages = [item.page for item in items]
    labels_by_page = {item.page: item.label for item in items}

    assert GuiPage.HISTORICAL_DATA in pages
    assert labels_by_page[GuiPage.HISTORICAL_DATA] == "Historical Data"
    assert pages.index(GuiPage.MARKET_DATA) < pages.index(GuiPage.HISTORICAL_DATA)
    assert pages.index(GuiPage.HISTORICAL_DATA) < pages.index(GuiPage.DECISIONS)
