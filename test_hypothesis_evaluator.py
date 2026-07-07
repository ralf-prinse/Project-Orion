from datetime import datetime

from models.hypothesis_evaluation_context import (
    HypothesisEvaluationContext,
)
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_evaluator import HypothesisEvaluator


def build_hypothesis(
    direction: str,
    minimum_sample_size: int,
    metric: str,
) -> StrategyHypothesis:
    return StrategyHypothesis(
        hypothesis_id="HYP-001",
        title="Test Hypothesis",
        description="Regression test.",
        metric_name=metric,
        expected_direction=direction,
        minimum_sample_size=minimum_sample_size,
        created_at=datetime(2026, 7, 7),
    )


def test_supported_hypothesis():
    hypothesis = build_hypothesis(
        direction="INCREASE",
        minimum_sample_size=10,
        metric="win_rate",
    )

    context = HypothesisEvaluationContext(
        hypothesis=hypothesis,
        sample_size=12,
        metric_value=0.58,
        expected_value=0.55,
    )

    result = HypothesisEvaluator().evaluate(context)

    assert result.status == "SUPPORTED"
    assert result.supported is True
    assert result.sufficient_data is True


def test_rejected_hypothesis():
    hypothesis = build_hypothesis(
        direction="DECREASE",
        minimum_sample_size=10,
        metric="max_drawdown",
    )

    context = HypothesisEvaluationContext(
        hypothesis=hypothesis,
        sample_size=12,
        metric_value=0.12,
        expected_value=0.08,
    )

    result = HypothesisEvaluator().evaluate(context)

    assert result.status == "REJECTED"
    assert result.supported is False
    assert result.sufficient_data is True


def test_insufficient_data():
    hypothesis = build_hypothesis(
        direction="INCREASE",
        minimum_sample_size=20,
        metric="average_profit",
    )

    context = HypothesisEvaluationContext(
        hypothesis=hypothesis,
        sample_size=5,
        metric_value=12.0,
        expected_value=10.0,
    )

    result = HypothesisEvaluator().evaluate(context)

    assert result.status == "INSUFFICIENT_DATA"
    assert result.supported is False
    assert result.sufficient_data is False