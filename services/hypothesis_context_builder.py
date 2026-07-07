from __future__ import annotations

from models.hypothesis_evaluation_context import (
    HypothesisEvaluationContext,
)
from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis


class HypothesisContextBuilder:
    """
    Builds HypothesisEvaluationContext from existing performance analysis.

    No AI.
    No trading decisions.
    No configuration changes.
    """

    def build(
        self,
        hypothesis: StrategyHypothesis,
        performance: PerformanceAnalysisResult,
        expected_value: float,
    ) -> HypothesisEvaluationContext:

        metric_value = self._metric_value(
            hypothesis=hypothesis,
            performance=performance,
        )

        return HypothesisEvaluationContext(
            hypothesis=hypothesis,
            sample_size=performance.total_trades,
            metric_value=metric_value,
            expected_value=expected_value,
        )

    def _metric_value(
        self,
        hypothesis: StrategyHypothesis,
        performance: PerformanceAnalysisResult,
    ) -> float:

        metric_name = hypothesis.metric_name

        if not hasattr(performance, metric_name):
            raise ValueError(
                f"PerformanceAnalysisResult heeft geen metric: {metric_name}"
            )

        return float(
            getattr(
                performance,
                metric_name,
            )
        )