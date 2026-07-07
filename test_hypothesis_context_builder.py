from datetime import datetime

from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_context_builder import (
    HypothesisContextBuilder,
)


def build_performance() -> PerformanceAnalysisResult:
    return PerformanceAnalysisResult(
        total_trades=100,
        win_rate=0.61,
        average_profit=145.0,
        average_loss=-82.0,
        profit_factor=1.82,
        expectancy=18.4,
        max_drawdown=0.11,
        total_return=0.27,
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
        expected_value=0.55,
    )

    assert context.hypothesis is hypothesis
    assert context.sample_size == 100
    assert context.metric_value == 0.61
    assert context.expected_value == 0.55


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