from models.performance_analysis_result import PerformanceAnalysisResult
from services.learning_pipeline import LearningPipeline


def build_analysis() -> PerformanceAnalysisResult:
    return PerformanceAnalysisResult(
        total_trades=100,
        winning_trades=58,
        losing_trades=42,
        win_rate=58.0,
        total_realized_profit_loss=850.0,
        total_unrealized_profit_loss=0.0,
        average_realized_profit_loss=8.5,
        average_return_percent=2.4,
        best_trade_symbol="NVDA",
        best_trade_return_percent=9.8,
        worst_trade_symbol="TSLA",
        worst_trade_return_percent=-4.2,
        average_confidence=0.78,
        average_expected_risk=2.1,
        profitable_confidence_threshold=0.73,
        dominant_regime="BULL",
        dominant_volatility="NORMAL",
        summary="Learning pipeline regression test.",
    )


def test_learning_pipeline_returns_result():
    pipeline = LearningPipeline()

    result = pipeline.run(
        performance=build_analysis(),
    )

    assert result.performance.total_trades == 100

    assert result.recommendations is not None

    assert result.idea_count >= 1

    assert result.has_ideas is True


def test_learning_pipeline_preserves_performance():
    pipeline = LearningPipeline()

    analysis = build_analysis()

    result = pipeline.run(
        performance=analysis,
    )

    assert result.performance is analysis


def test_learning_pipeline_generates_unique_ids():
    pipeline = LearningPipeline()

    result = pipeline.run(
        performance=build_analysis(),
    )

    ids = [
        idea.idea_id
        for idea in result.ideas
    ]

    assert len(ids) == len(set(ids))