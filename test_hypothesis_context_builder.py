from datetime import datetime

from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_context_builder import (
    HypothesisContextBuilder,
)


def build_performance() -> PerformanceAnalysisResult:
    return PerformanceAnalysisResult(
        total_trades=100,
        winning_trades=61,
        losing_trades=39,
        win_rate=61.0,
        total_realized_profit_loss=1840.0,
        total_unrealized_profit_loss=0.0,
        average_realized_profit_loss=18.4,
        average_return_percent=0.27,
        best_trade_symbol="BEST",
        best_trade_return_percent=8.0,
        worst_trade_symbol="WORST",
        worst_trade_return_percent=-4.0,
        average_confidence=0.78,
        average_expected_risk=0.11,
        profitable_confidence_threshold=0.75,
        dominant_regime="BULL",
        dominant_volatility="LOW",
        summary="Canonical hypothesis context fixture.",
    )


def test_build_context_from_performance():
    hypothesis = StrategyHypothesis(
        hypothesis_id="HYP-001",
        title="Increase win rate",
        description="Win rate should exceed the target.",
        metric_name="win_rate",
        expected_direction="INCREASE",
        minimum_sample_size=50,
        created_at=datetime(2026, 7, 7),
    )

    context = HypothesisContextBuilder().build(
        hypothesis=hypothesis,
        performance=build_performance(),
        expected_value=55.0,
    )

    assert context.hypothesis is hypothesis
    assert context.sample_size == 100
    assert context.metric_value == 61.0
    assert context.expected_value == 55.0


def test_unknown_metric_raises():
    hypothesis = StrategyHypothesis(
        hypothesis_id="HYP-002",
        title="Unknown metric",
        description="Regression test.",
        metric_name="does_not_exist",
        expected_direction="INCREASE",
        minimum_sample_size=10,
        created_at=datetime(2026, 7, 7),
    )

    try:
        HypothesisContextBuilder().build(
            hypothesis=hypothesis,
            performance=build_performance(),
            expected_value=1.0,
        )
    except ValueError as exc:
        assert "does_not_exist" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
