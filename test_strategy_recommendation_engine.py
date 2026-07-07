from __future__ import annotations

from models.performance_analysis_result import PerformanceAnalysisResult
from services.strategy_recommendation_engine import (
    StrategyRecommendationEngine,
)


def _analysis(
    total_trades: int = 10,
    win_rate: float = 40.0,
    total_realized_profit_loss: float = -25.0,
    average_expected_risk: float = 6.0,
    profitable_confidence_threshold: float | None = 0.85,
) -> PerformanceAnalysisResult:
    return PerformanceAnalysisResult(
        total_trades=total_trades,
        winning_trades=4,
        losing_trades=6,
        win_rate=win_rate,
        total_realized_profit_loss=total_realized_profit_loss,
        total_unrealized_profit_loss=0.0,
        average_realized_profit_loss=-2.5,
        average_return_percent=-2.5,
        best_trade_symbol="AAA",
        best_trade_return_percent=5.0,
        worst_trade_symbol="BBB",
        worst_trade_return_percent=-10.0,
        average_confidence=0.80,
        average_expected_risk=average_expected_risk,
        profitable_confidence_threshold=profitable_confidence_threshold,
        dominant_regime="BULL",
        dominant_volatility="LOW",
        summary="Test analysis summary.",
    )


def main():
    engine = StrategyRecommendationEngine()

    result = engine.build(
        _analysis()
    )

    titles = [
        recommendation.title
        for recommendation in result.recommendations
    ]

    assert "Increase confidence threshold" in titles
    assert "Reduce position exposure" in titles
    assert "Avoid high expected risk setups" in titles
    assert "Use profitable confidence floor" in titles

    ordered = result.ordered

    assert ordered[0].priority <= ordered[-1].priority

    empty_result = engine.build(
        _analysis(
            total_trades=0,
            win_rate=0.0,
            total_realized_profit_loss=0.0,
            average_expected_risk=0.0,
            profitable_confidence_threshold=None,
        )
    )

    assert len(empty_result.recommendations) == 1
    assert empty_result.recommendations[0].title == (
        "Collect more trading data"
    )

    stable_result = engine.build(
        _analysis(
            total_trades=10,
            win_rate=70.0,
            total_realized_profit_loss=50.0,
            average_expected_risk=1.0,
            profitable_confidence_threshold=0.70,
        )
    )

    assert len(stable_result.recommendations) == 1
    assert stable_result.recommendations[0].title == (
        "Maintain current configuration"
    )

    print("STRATEGY RECOMMENDATION ENGINE: PASS ✅")


if __name__ == "__main__":
    main()