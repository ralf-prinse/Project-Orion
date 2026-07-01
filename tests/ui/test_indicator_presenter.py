from services.analysis.models import IndicatorResult
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.indicator_presenter import IndicatorPresenter
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry


def _sample_indicators() -> IndicatorResult:
    result = IndicatorResult(symbol="aapl")
    result.set("sma20", 182.123456)
    result.set("sma50", 176.5)
    result.set("ema20", 184.0)
    result.set("ema50", 177.25)
    result.set("adx14", 28.4)
    result.set("rsi14", 61.3456)
    result.set("macd", {"histogram": 0.75, "line": 1.25, "signal": 0.5})
    result.set("atr14", 3.125)
    result.set("bollinger", {"lower": 170.0, "middle": 181.0, "upper": 192.0})
    result.set("latest_close", 185.0)
    result.set("recent_high_20", 190.0)
    result.set("recent_low_20", 172.0)
    result.set("latest_volume", 32000000.0)
    result.set("average_volume_20", 28000000.0)
    result.set("relative_volume_20", 1.142857)
    result.set("relative_strength_20", 4.25)
    result.set("relative_strength_50", 7.5)
    return result


def test_indicator_presenter_creates_stable_dashboard_sections():
    sections = IndicatorPresenter().create_sections(_sample_indicators())

    assert [section.title for section in sections] == [
        "Indicator Dashboard",
        "Trend Indicators",
        "Momentum Indicators",
        "Volatility Indicators",
        "Structure, Volume and Relative Strength",
    ]
    assert sections[0].metrics[0].value == "AAPL"
    assert sections[0].metrics[1].value == "17"
    assert sections[1].metrics[0].value == "182.1235"
    assert sections[2].metrics[1].value == "histogram=0.7500, line=1.2500, signal=0.5000"


def test_indicator_presenter_marks_missing_values_without_calculating_them():
    result = IndicatorResult(symbol="MSFT")

    sections = IndicatorPresenter().create_sections(result)

    assert sections[0].metrics[0].value == "MSFT"
    assert sections[0].metrics[1].value == "0"
    assert sections[1].metrics[0].value == "N/A"
    assert sections[2].metrics[0].value == "N/A"


def test_gui_shell_builds_indicator_dashboard_without_calculating_indicators():
    state = GuiShell().build_indicator_dashboard(_sample_indicators())

    assert state.current_page == GuiPage.INDICATORS
    assert state.status_message == "Indicator dashboard updated"
    assert state.sections[0].title == "Indicator Dashboard"
    assert state.sections[1].title == "Trend Indicators"


def test_dashboard_composer_can_include_indicator_result():
    sections = DashboardComposer().compose(indicator_result=_sample_indicators())

    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "Indicators"
    assert sections[0].metrics[1].value == "1"
    assert sections[1].title == "Indicator Dashboard"


def test_navigation_registry_contains_indicators_page_between_analysis_and_signals():
    items = NavigationRegistry().get_items()
    pages = [item.page for item in items]
    labels_by_page = {item.page: item.label for item in items}

    assert GuiPage.INDICATORS in pages
    assert labels_by_page[GuiPage.INDICATORS] == "Indicators"
    assert pages.index(GuiPage.ANALYSIS) < pages.index(GuiPage.INDICATORS)
    assert pages.index(GuiPage.INDICATORS) < pages.index(GuiPage.SIGNALS)
