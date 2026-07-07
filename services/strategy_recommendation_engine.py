from __future__ import annotations

from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_recommendation import (
    StrategyRecommendation,
    StrategyRecommendationResult,
)


class StrategyRecommendationEngine:
    """
    Deterministic recommendation engine.

    Converts performance analysis into self-improvement suggestions.

    Recommendations are informational only.
    They do not modify configuration automatically.
    """

    def build(
        self,
        analysis: PerformanceAnalysisResult,
    ) -> StrategyRecommendationResult:
        recommendations: list[StrategyRecommendation] = []

        if analysis.total_trades == 0:
            recommendations.append(
                StrategyRecommendation(
                    title="Collect more trading data",
                    description=(
                        "ORION has no journal entries yet. "
                        "Run more autonomous paper trading cycles before "
                        "changing strategy parameters."
                    ),
                    priority=1,
                    confidence=1.0,
                    expected_impact=0.0,
                    category="DATA",
                    rationale="No historical performance data is available.",
                )
            )

            return StrategyRecommendationResult(
                recommendations=recommendations,
            )

        if analysis.win_rate < 50.0:
            recommendations.append(
                StrategyRecommendation(
                    title="Increase confidence threshold",
                    description=(
                        "The current win rate is below 50%. "
                        "ORION should consider requiring stronger BUY "
                        "signals before allocating capital."
                    ),
                    priority=1,
                    confidence=0.85,
                    expected_impact=0.75,
                    category="RISK_CONTROL",
                    rationale=(
                        f"Observed win rate is {analysis.win_rate:.2f}%."
                    ),
                )
            )

        if analysis.total_realized_profit_loss < 0:
            recommendations.append(
                StrategyRecommendation(
                    title="Reduce position exposure",
                    description=(
                        "Realized P/L is negative. ORION should consider "
                        "lowering max position value until performance "
                        "improves."
                    ),
                    priority=2,
                    confidence=0.80,
                    expected_impact=0.65,
                    category="POSITION_SIZING",
                    rationale=(
                        "Total realized P/L is "
                        f"{analysis.total_realized_profit_loss:.2f}."
                    ),
                )
            )

        if analysis.average_expected_risk > 5.0:
            recommendations.append(
                StrategyRecommendation(
                    title="Avoid high expected risk setups",
                    description=(
                        "Average expected risk is elevated. ORION should "
                        "prefer candidates with lower expected risk."
                    ),
                    priority=3,
                    confidence=0.75,
                    expected_impact=0.55,
                    category="RISK_MANAGEMENT",
                    rationale=(
                        "Average expected risk is "
                        f"{analysis.average_expected_risk:.6f}."
                    ),
                )
            )

        if (
            analysis.profitable_confidence_threshold is not None
            and analysis.profitable_confidence_threshold > 0.80
        ):
            recommendations.append(
                StrategyRecommendation(
                    title="Use profitable confidence floor",
                    description=(
                        "Profitable trades only appeared above a higher "
                        "confidence level. ORION should consider using this "
                        "as a minimum BUY threshold."
                    ),
                    priority=2,
                    confidence=0.70,
                    expected_impact=0.60,
                    category="CONFIDENCE_THRESHOLD",
                    rationale=(
                        "Lowest profitable confidence observed: "
                        f"{analysis.profitable_confidence_threshold:.4f}."
                    ),
                )
            )

        if not recommendations:
            recommendations.append(
                StrategyRecommendation(
                    title="Maintain current configuration",
                    description=(
                        "Current performance does not indicate an obvious "
                        "need for parameter changes."
                    ),
                    priority=5,
                    confidence=0.65,
                    expected_impact=0.20,
                    category="MAINTENANCE",
                    rationale=analysis.summary,
                )
            )

        return StrategyRecommendationResult(
            recommendations=recommendations,
        )