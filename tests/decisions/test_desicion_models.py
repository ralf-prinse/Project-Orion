from services.decisions.models import (
    DecisionAction,
    DecisionContext,
    DecisionResult,
    DecisionState,
)


def test_decision_context_has_safe_defaults():
    context = DecisionContext()

    assert context.available_cash == 0.0
    assert context.portfolio_value == 0.0
    assert context.open_positions == 0
    assert context.max_positions == 0
    assert context.risk_profile == "default"


def test_decision_state_tracks_reasons_and_warnings():
    state = DecisionState(symbol="TEST")

    state.add_reason("Signal is valid.")
    state.add_warning("Portfolio is full.")

    assert state.symbol == "TEST"
    assert state.proposed_action == DecisionAction.SKIP
    assert state.reasons == ["Signal is valid."]
    assert state.warnings == ["Portfolio is full."]


def test_decision_result_has_safe_defaults():
    result = DecisionResult(symbol="TEST")

    assert result.symbol == "TEST"
    assert result.action == DecisionAction.SKIP
    assert result.confidence == 0
    assert result.position_size == 0.0
    assert result.risk_level == 0
    assert result.reasons == []
    assert result.warnings == []