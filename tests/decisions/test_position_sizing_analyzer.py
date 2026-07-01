from services.decisions.analyzers.position_sizing_analyzer import PositionSizingAnalyzer
from services.decisions.models import DecisionContext, DecisionState
from services.signals.models import Signal, SignalResult


def test_position_sizing_calculates_recommended_shares_for_buy_signal():
    analyzer = PositionSizingAnalyzer()
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
    decision_state = DecisionState(
        symbol="AAPL",
        signal_valid=True,
        portfolio_allowed=True,
        risk_allowed=True,
    )

    result = analyzer.analyze(
        signal_result=signal_result,
        decision_context=decision_context,
        decision_state=decision_state,
    )

    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 20
    assert result.position_sizing.position_value == 2000.0
    assert result.position_sizing.risk_amount == 100.0
    assert result.position_sizing.risk_per_share == 5.0
    assert result.position_size == 20.0
    assert "Position sizing calculated using fixed fractional risk model." in result.reasons


def test_position_sizing_respects_available_cash_limit():
    analyzer = PositionSizingAnalyzer()
    signal_result = SignalResult(
        symbol="AAPL",
        signal=Signal.BUY,
        confidence=90,
    )
    decision_context = DecisionContext(
        available_cash=450,
        portfolio_value=10_000,
        entry_price=100,
        stop_loss=95,
        risk_per_trade=0.01,
    )
    decision_state = DecisionState(
        symbol="AAPL",
        signal_valid=True,
        portfolio_allowed=True,
        risk_allowed=True,
    )

    result = analyzer.analyze(
        signal_result=signal_result,
        decision_context=decision_context,
        decision_state=decision_state,
    )

    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 4
    assert result.position_sizing.position_value == 400.0
    assert result.position_size == 4.0


def test_position_sizing_respects_max_position_value_limit():
    analyzer = PositionSizingAnalyzer()
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
        max_position_value=500,
    )
    decision_state = DecisionState(
        symbol="AAPL",
        signal_valid=True,
        portfolio_allowed=True,
        risk_allowed=True,
    )

    result = analyzer.analyze(
        signal_result=signal_result,
        decision_context=decision_context,
        decision_state=decision_state,
    )

    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 5
    assert result.position_sizing.position_value == 500.0
    assert result.position_size == 5.0


def test_position_sizing_skips_when_stop_loss_is_invalid():
    analyzer = PositionSizingAnalyzer()
    signal_result = SignalResult(
        symbol="AAPL",
        signal=Signal.BUY,
        confidence=90,
    )
    decision_context = DecisionContext(
        available_cash=10_000,
        portfolio_value=10_000,
        entry_price=100,
        stop_loss=105,
        risk_per_trade=0.01,
    )
    decision_state = DecisionState(
        symbol="AAPL",
        signal_valid=True,
        portfolio_allowed=True,
        risk_allowed=True,
    )

    result = analyzer.analyze(
        signal_result=signal_result,
        decision_context=decision_context,
        decision_state=decision_state,
    )

    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 0
    assert result.position_size == 0.0
    assert "Position sizing skipped; stop loss must be below entry price." in result.warnings


def test_position_sizing_skips_non_long_entry_signal():
    analyzer = PositionSizingAnalyzer()
    signal_result = SignalResult(
        symbol="AAPL",
        signal=Signal.SELL,
        confidence=90,
    )
    decision_context = DecisionContext(
        available_cash=10_000,
        portfolio_value=10_000,
        entry_price=100,
        stop_loss=95,
        risk_per_trade=0.01,
    )
    decision_state = DecisionState(
        symbol="AAPL",
        signal_valid=True,
        portfolio_allowed=True,
        risk_allowed=True,
    )

    result = analyzer.analyze(
        signal_result=signal_result,
        decision_context=decision_context,
        decision_state=decision_state,
    )

    assert result.position_sizing is not None
    assert result.position_sizing.recommended_shares == 0
    assert result.position_size == 0.0
    assert (
        "Position sizing skipped because signal does not require a new long position."
        in result.warnings
    )
