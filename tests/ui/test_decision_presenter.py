from services.decisions.models import DecisionAction, DecisionResult, PositionSizingResult
from ui.foundation.decision_presenter import DecisionPresenter
from ui.foundation.gui_shell import GuiShell
from ui.foundation.models import GuiPage


def test_decision_presenter_creates_summary_and_position_sections():
    decision = DecisionResult(
        symbol="aapl",
        action=DecisionAction.BUY,
        confidence=87,
        risk_level=2,
        position_size=1500.0,
        position_sizing=PositionSizingResult(
            recommended_shares=10,
            position_value=1500.0,
            risk_amount=100.0,
            risk_per_share=10.0,
            capital_used=0.15,
        ),
    )

    sections = DecisionPresenter().create_sections(decision)

    assert sections[0].title == "Decision Dashboard"
    assert sections[0].metrics[0].value == "AAPL"
    assert sections[0].metrics[1].value == "BUY"
    assert sections[0].metrics[2].value == "87"
    assert sections[1].title == "Decision Position Sizing"
    assert sections[1].metrics[1].value == "10"
    assert sections[1].metrics[2].value == "1500.00"


def test_decision_presenter_handles_missing_position_sizing_deterministically():
    decision = DecisionResult(symbol="MSFT", action=DecisionAction.WATCH)

    sections = DecisionPresenter().create_sections(decision)

    assert sections[1].metrics[1].value == "0"
    assert sections[1].metrics[2].value == "0.00"
    assert sections[1].metrics[4].value == "N/A"


def test_decision_presenter_adds_diagnostics_when_available():
    sizing = PositionSizingResult(warnings=["Position capped by capital limit"])
    decision = DecisionResult(
        symbol="NVDA",
        reasons=["Signal passed validation"],
        warnings=["Portfolio capacity limited"],
        position_sizing=sizing,
    )

    sections = DecisionPresenter().create_sections(decision)
    diagnostics = sections[-1]

    assert diagnostics.title == "Decision Diagnostics"
    assert diagnostics.metrics[0].value == "Signal passed validation"
    assert diagnostics.metrics[1].value == "Portfolio capacity limited"
    assert diagnostics.metrics[2].value == "Position capped by capital limit"


def test_gui_shell_builds_decision_dashboard():
    shell = GuiShell()
    decision = DecisionResult(symbol="TSLA", action=DecisionAction.SKIP, confidence=12)

    state = shell.build_decision_dashboard(decision)

    assert state.current_page == GuiPage.DECISIONS
    assert state.status_message == "Decision dashboard updated"
    assert state.sections[0].title == "Decision Dashboard"
