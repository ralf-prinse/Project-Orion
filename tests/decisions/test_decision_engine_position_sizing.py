from services.decisions.engine.decision_engine import DecisionEngine
from services.decisions.models import DecisionAction, DecisionContext
from services.signals.models import Signal, SignalResult


def test_decision_engine_integrates_position_sizing_for_buy_signal():
    engine = DecisionEngine()
    signal_result = SignalResult(
        symbol="AAPL",
        signal=Signal.BUY,
        confidence=90,
    )
    decision_context = DecisionContext(
        available_cash=10_000,
        portfolio_value=10_000,
        entry_price=100,
        stop_loss=95,
        risk_per_trade=0.01,
    )

    result = engine.decide(
        signal_result=signal_result,
        decision_context=decision_context,
    )

    assert result.action == DecisionAction.BUY
    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 20
    assert result.position_size == 20.0
    assert "Position sizing calculated using fixed fractional risk model." in result.reasons


def test_decision_engine_keeps_buy_decision_when_position_sizing_context_missing():
    engine = DecisionEngine()
    signal_result = SignalResult(
        symbol="AAPL",
        signal=Signal.BUY,
        confidence=90,
    )

    result = engine.decide(signal_result=signal_result)

    assert result.action == DecisionAction.BUY
    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 0
    assert result.position_size == 0.0
    assert "Position sizing skipped; account equity is not configured." in result.warnings
