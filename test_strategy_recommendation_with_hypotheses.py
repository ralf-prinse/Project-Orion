from datetime import datetime

from models.hypothesis_evaluation import HypothesisEvaluation
from models.hypothesis_evaluation_report import (
    HypothesisEvaluationReport,
)
from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis
from services.strategy_recommendation_engine import (
    StrategyRecommendationEngine,
)


def build_analysis() -> PerformanceAnalysisResult:
    return PerformanceAnalysisResult(
        total_trades=25,
        winning_trades=15,
        losing_trades=10,
        win_rate=60.0,
        total_realized_profit_loss=250.0,
        total_unrealized_profit_loss=0.0,
        average_realized_profit_loss=10.0,
        average_return_percent=2.5,
        best_trade_symbol="AAPL",
        best_trade_return_percent=8.0,
        worst_trade_symbol="MSFT",
        worst_trade_return_percent=-4.0,
        average_confidence=0.72,
        average_expected_risk=2.0,
        profitable_confidence_threshold=0.70,
        dominant_regime="BULL",
        dominant_volatility="NORMAL",
        summary="Regression analysis.",
    )


def build_hypothesis() -> StrategyHypothesis:
    return StrategyHypothesis(
        hypothesis_id="HYP-001",
        title="Improve win rate",
        description="Regression hypothesis.",
        metric_name="win_rate",
        expected_direction="INCREASE",
        minimum_sample_size=50,
        created_at=datetime(2026, 7, 7),
    )


def build_report() -> HypothesisEvaluationReport:
    hypothesis = build_hypothesis()

    return HypothesisEvaluationReport(
        evaluations=[
            HypothesisEvaluation(
                hypothesis=hypothesis,
                sample_size=25,
                metric_value=60.0,
                expected_value=65.0,
                confidence=0.50,
                supported=False,
                status="INSUFFICIENT_DATA",
                reason="Regression test.",
            ),
            HypothesisEvaluation(
                hypothesis=hypothesis,
                sample_size=80,
                metric_value=48.0,
                expected_value=55.0,
                confidence=0.85,
                supported=False,
                status="REJECTED",
                reason="Regression test.",
            ),
        ],
    )


def test_recommendations_include_hypothesis_findings():
    result = StrategyRecommendationEngine().build(
        analysis=build_analysis(),
        hypothesis_report=build_report(),
    )

    categories = [
        recommendation.category
        for recommendation in result.recommendations
    ]

    assert "HYPOTHESIS_DATA" in categories
    assert "HYPOTHESIS_REVIEW" in categories