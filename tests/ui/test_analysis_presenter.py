from services.analysis.models import AnalysisResult
from ui.foundation.analysis_presenter import AnalysisPresenter
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry


def _sample_analysis() -> AnalysisResult:
    result = AnalysisResult(
        symbol="aapl",
        trend_score=88,
        momentum_score=76,
        volatility_score=62,
        structure_score=81,
        volume_score=70,
        market_regime_score=55,
        relative_strength_score=84,
        candlestick_score=66,
        overall_score=79,
    )
    result.add_note("TrendAnalyzer detected a bullish trend.")
    result.add_note("CandlestickPatternAnalyzer detected supportive price action.")
    return result


def test_analysis_presenter_creates_summary_score_and_notes_sections():
    sections = AnalysisPresenter().create_sections(_sample_analysis())

    assert [section.title for section in sections] == [
        "Analysis Dashboard",
        "Analysis Scores",
        "Analysis Notes",
    ]
    assert sections[0].metrics[0].value == "AAPL"
    assert sections[0].metrics[1].value == "79"
    assert [metric.value for metric in sections[1].metrics] == [
        "88",
        "76",
        "62",
        "81",
        "70",
        "55",
        "84",
        "66",
    ]


def test_analysis_presenter_omits_notes_section_when_empty():
    result = AnalysisResult(symbol="MSFT", overall_score=63)

    sections = AnalysisPresenter().create_sections(result)

    assert [section.title for section in sections] == [
        "Analysis Dashboard",
        "Analysis Scores",
    ]


def test_gui_shell_builds_analysis_dashboard_without_calculating_analysis():
    state = GuiShell().build_analysis_dashboard(_sample_analysis())

    assert state.current_page == GuiPage.ANALYSIS
    assert state.status_message == "Analysis dashboard updated"
    assert state.sections[0].title == "Analysis Dashboard"
    assert state.sections[1].title == "Analysis Scores"


def test_dashboard_composer_can_include_analysis_result():
    sections = DashboardComposer().compose(analysis_result=_sample_analysis())

    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "Analysis"
    assert sections[0].metrics[1].value == "1"
    assert sections[1].title == "Analysis Dashboard"


def test_navigation_registry_contains_analysis_page_between_decision_and_signal():
    items = NavigationRegistry().get_items()
    pages = [item.page for item in items]
    labels_by_page = {item.page: item.label for item in items}

    assert GuiPage.ANALYSIS in pages
    assert labels_by_page[GuiPage.ANALYSIS] == "Analysis"
    assert pages.index(GuiPage.DECISIONS) < pages.index(GuiPage.ANALYSIS)
    assert pages.index(GuiPage.ANALYSIS) < pages.index(GuiPage.SIGNALS)
