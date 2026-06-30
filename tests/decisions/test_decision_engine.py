from services.decisions.engine import DecisionEngine
from services.decisions.models import DecisionAction, DecisionContext
from services.signals.models import Signal, SignalResult


def make_signal_result(
    symbol="TEST",
    signal=Signal.IGNORE,
    confidence=0,
):
    return SignalResult(
        symbol=symbol,
        signal=signal,
        confidence=confidence,
    )


def test_decision_engine_skips_ignore_signal():
    signal_result = make_signal_result(
        signal=Signal.IGNORE,
        confidence=0,
    )

    engine = DecisionEngine()

    result = engine.decide(signal_result)

    assert result.symbol == "TEST"
    assert result.action == DecisionAction.SKIP
    assert result.confidence == 0
    assert "Signal is IGNORE; no decision action allowed." in result.warnings
    assert "Decision skipped because signal is invalid." in result.warnings


def test_decision_engine_converts_buy_signal_to_buy_decision():
    signal_result = make_signal_result(
        signal=Signal.BUY,
        confidence=75,
    )

    engine = DecisionEngine()

    result = engine.decide(signal_result)

    assert result.symbol == "TEST"
    assert result.action == DecisionAction.BUY
    assert result.confidence == 75
    assert "Signal BUY is valid." in result.reasons
    assert (
        "Portfolio validation skipped; no max position limit configured."
        in result.reasons
    )
    assert "Risk validation passed." in result.reasons
    assert "Decision action assembled as BUY." in result.reasons
    assert result.warnings == []


def test_decision_engine_converts_watch_signal_to_watch_decision():
    signal_result = make_signal_result(
        signal=Signal.WATCH,
        confidence=55,
    )

    engine = DecisionEngine()

    result = engine.decide(signal_result)

    assert result.action == DecisionAction.WATCH
    assert result.confidence == 55
    assert "Signal WATCH is valid." in result.reasons


def test_decision_engine_accepts_decision_context():
    signal_result = make_signal_result(
        signal=Signal.BUY,
        confidence=80,
    )

    context = DecisionContext(
        available_cash=10000.0,
        portfolio_value=50000.0,
        open_positions=2,
        max_positions=10,
    )

    engine = DecisionEngine()

    result = engine.decide(
        signal_result=signal_result,
        decision_context=context,
    )

    assert result.action == DecisionAction.BUY
    assert result.confidence == 80
    assert "Portfolio validation passed." in result.reasons


def test_decision_engine_blocks_when_portfolio_is_full():
    signal_result = make_signal_result(
        signal=Signal.BUY,
        confidence=80,
    )

    context = DecisionContext(
        open_positions=5,
        max_positions=5,
    )

    engine = DecisionEngine()

    result = engine.decide(
        signal_result=signal_result,
        decision_context=context,
    )

    assert result.action == DecisionAction.SKIP
    assert result.confidence == 80
    assert (
        "Portfolio validation blocked decision; maximum positions reached."
        in result.warnings
    )
    assert "Decision skipped because portfolio rules blocked it." in result.warnings


def test_decision_engine_blocks_when_risk_profile_is_blocked():
    signal_result = make_signal_result(
        signal=Signal.BUY,
        confidence=80,
    )

    context = DecisionContext(
        risk_profile="blocked",
    )

    engine = DecisionEngine()

    result = engine.decide(
        signal_result=signal_result,
        decision_context=context,
    )

    assert result.action == DecisionAction.SKIP
    assert result.confidence == 80
    assert "Risk validation blocked decision; risk profile is blocked." in result.warnings
    assert "Decision skipped because risk rules blocked it." in result.warnings