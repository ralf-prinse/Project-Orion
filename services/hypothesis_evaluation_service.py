from __future__ import annotations

from models.hypothesis_evaluation import HypothesisEvaluation
from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_hypothesis import StrategyHypothesis
from services.hypothesis_context_builder import HypothesisContextBuilder
from services.hypothesis_evaluator import HypothesisEvaluator


class HypothesisEvaluationService:
    """
    Evaluates multiple strategy hypotheses against one performance result.

    No AI.
    No trading decisions.
    No configuration changes.
    """

    def __init__(
        self,
        context_builder: HypothesisContextBuilder | None = None,
        evaluator: HypothesisEvaluator | None = None,
    ):
        self.context_builder = context_builder or HypothesisContextBuilder()
        self.evaluator = evaluator or HypothesisEvaluator()

    def evaluate_all(
        self,
        hypotheses: list[StrategyHypothesis],
        performance: PerformanceAnalysisResult,
        expected_values: dict[str, float],
    ) -> list[HypothesisEvaluation]:

        evaluations: list[HypothesisEvaluation] = []

        for hypothesis in hypotheses:
            expected_value = expected_values.get(
                hypothesis.hypothesis_id,
            )

            if expected_value is None:
                raise ValueError(
                    "Missing expected value for hypothesis: "
                    f"{hypothesis.hypothesis_id}"
                )

            context = self.context_builder.build(
                hypothesis=hypothesis,
                performance=performance,
                expected_value=expected_value,
            )

            evaluations.append(
                self.evaluator.evaluate(context)
            )

        return evaluations