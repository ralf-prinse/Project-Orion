from datetime import datetime

from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_evaluation_service import (
    HypothesisEvaluationService,
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


def build_hypotheses() -> list[StrategyHypothesis]:
    return [
        StrategyHypothesis(
            hypothesis_id="WIN_RATE",
            title="Increase win rate",
            description="Win rate should improve.",
            metric_name="win_rate",
            expected_direction="INCREASE",
            minimum_sample_size=50,
            created_at=datetime(2026, 7, 7),
        ),
        StrategyHypothesis(
            hypothesis_id="DRAWDOWN",
            title="Reduce drawdown",
            description="Drawdown should decrease.",
            metric_name="max_drawdown",
            expected_direction="DECREASE",
            minimum_sample_size=50,
            created_at=datetime(2026, 7, 7),
        ),
    ]


def test_evaluate_multiple_hypotheses():
    service = HypothesisEvaluationService()

    results = service.evaluate_all(
        hypotheses=build_hypotheses(),
        performance=build_performance(),
        expected_values={
            "WIN_RATE": 0.55,
            "DRAWDOWN": 0.15,
        },
    )

    assert len(results) == 2

    assert results[0].status == "SUPPORTED"
    assert results[0].supported is True

    assert results[1].status == "SUPPORTED"
    assert results[1].supported is True


def test_missing_expected_value():
    service = HypothesisEvaluationService()

    try:
        service.evaluate_all(
            hypotheses=build_hypotheses(),
            performance=build_performance(),
            expected_values={
                "WIN_RATE": 0.55,
            },
        )
    except ValueError as exc:
        assert "DRAWDOWN" in str(exc)
    else:
        raise AssertionError("Expected ValueError")