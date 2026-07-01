from services.signals.models import Signal, SignalResult
from ui.foundation.dashboard_composer import DashboardComposer
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage
from ui.foundation.navigation import NavigationRegistry
from ui.foundation.signal_presenter import SignalPresenter


def _sample_signal() -> SignalResult:
    result = SignalResult(
        symbol="aapl",
        signal=Signal.BUY,
        confidence=82,
        bullish_score=82,
        bearish_score=12,
        neutral_score=18,
    )
    result.add_note("BUY signal detected by EntrySignalAnalyzer.")
    result.add_note("Final signal: BUY with confidence 82")
    return result


def test_signal_presenter_creates_summary_and_score_sections():
    sections = SignalPresenter().create_sections(_sample_signal())

    assert [section.title for section in sections] == [
        "Signal Dashboard",
        "Signal Scores",
        "Signal Notes",
    ]
    assert sections[0].metrics[0].value == "AAPL"
    assert sections[0].metrics[1].value == "BUY"
    assert sections[0].metrics[2].value == "82"
    assert sections[1].metrics[0].value == "82"
    assert sections[1].metrics[1].value == "12"
    assert sections[1].metrics[2].value == "18"


def test_signal_presenter_omits_notes_section_when_empty():
    result = SignalResult(symbol="MSFT", signal=Signal.WATCH, confidence=61)

    sections = SignalPresenter().create_sections(result)

    assert [section.title for section in sections] == [
        "Signal Dashboard",
        "Signal Scores",
    ]


def test_gui_shell_builds_signal_dashboard_without_generating_signals():
    state = GuiShell().build_signal_dashboard(_sample_signal())

    assert state.current_page == GuiPage.SIGNALS
    assert state.status_message == "Signal dashboard updated"
    assert state.sections[0].title == "Signal Dashboard"
    assert state.sections[1].title == "Signal Scores"


def test_dashboard_composer_can_include_signal_result():
    sections = DashboardComposer().compose(signal_result=_sample_signal())

    assert sections[0].title == "Unified Dashboard Summary"
    assert sections[0].metrics[0].value == "Signals"
    assert sections[0].metrics[1].value == "1"
    assert sections[1].title == "Signal Dashboard"


def test_navigation_registry_contains_signal_page_between_decision_and_scanner():
    items = NavigationRegistry().get_items()
    pages = [item.page for item in items]
    labels_by_page = {item.page: item.label for item in items}

    assert GuiPage.SIGNALS in pages
    assert labels_by_page[GuiPage.SIGNALS] == "Signals"
    assert pages.index(GuiPage.DECISIONS) < pages.index(GuiPage.SIGNALS)
    assert pages.index(GuiPage.SIGNALS) < pages.index(GuiPage.SCANNER)
