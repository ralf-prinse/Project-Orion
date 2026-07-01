from services.ai.models import AIExplanationResult
from ui.foundation.explanation_presenter import ExplanationPresenter
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage


def test_explanation_presenter_creates_summary_section_for_valid_result():
    result = AIExplanationResult(
        symbol="AAPL",
        valid_explanation=True,
        summary="Deterministic explanation summary.",
        source_count=2,
    )
    presenter = ExplanationPresenter()

    sections = presenter.create_sections(result)

    assert len(sections) == 1
    assert sections[0].title == "AI Explanation Summary"
    assert [metric.value for metric in sections[0].metrics[:3]] == ["AAPL", "Valid", "2"]
    assert sections[0].metrics[3].value == "Deterministic explanation summary."


def test_explanation_presenter_creates_sections_from_explanation_bullets():
    result = AIExplanationResult(
        symbol="MSFT",
        valid_explanation=True,
        summary="Summary.",
        source_count=1,
    )
    result.add_section("Decision explanation", ["Beslissing: BUY.", "Confidence: 82."])
    presenter = ExplanationPresenter()

    sections = presenter.create_sections(result)

    assert len(sections) == 2
    assert sections[1].title == "Decision explanation"
    assert sections[1].metrics[0].label == "Bullet 1"
    assert sections[1].metrics[0].value == "Beslissing: BUY."
    assert sections[1].metrics[1].value == "Confidence: 82."


def test_explanation_presenter_adds_reasons_and_warnings_sections():
    result = AIExplanationResult(symbol="NVDA", summary="Summary.")
    result.add_reason("Uitleg is deterministisch.")
    result.add_warning("Geen trade plan beschikbaar.")
    presenter = ExplanationPresenter()

    sections = presenter.create_sections(result)

    assert [section.title for section in sections] == [
        "AI Explanation Summary",
        "Explanation Sources",
        "Explanation Warnings",
    ]
    assert sections[1].metrics[0].value == "Uitleg is deterministisch."
    assert sections[2].metrics[0].value == "Geen trade plan beschikbaar."


def test_gui_shell_build_explanation_updates_display_state_only():
    result = AIExplanationResult(
        symbol="AAPL",
        valid_explanation=True,
        summary="AI vat uitsluitend Orion-resultaten samen.",
        source_count=1,
    )
    shell = GuiShell()

    state = shell.build_explanation(result)

    assert state.current_page == GuiPage.DASHBOARD
    assert state.status_message == "Explanation updated"
    assert state.sections[0].title == "AI Explanation Summary"
    assert state.sections[0].metrics[0].value == "AAPL"
