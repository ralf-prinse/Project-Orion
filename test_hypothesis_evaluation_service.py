from datetime import datetime

from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_evaluation_service import (
    HypothesisEvaluationService,
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
        summary="Canonical hypothesis evaluation fixture.",
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
            hypothesis_id="EXPECTED_RISK",
            title="Reduce expected risk",
            description="Average expected risk should decrease.",
            metric_name="average_expected_risk",
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
            "WIN_RATE": 55.0,
            "EXPECTED_RISK": 0.15,
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
                "WIN_RATE": 55.0,
            },
        )
    except ValueError as exc:
        assert "EXPECTED_RISK" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
