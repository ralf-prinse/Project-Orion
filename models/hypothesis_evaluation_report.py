from __future__ import annotations

from dataclasses import dataclass

from models.hypothesis_evaluation import HypothesisEvaluation


@dataclass(frozen=True)
class HypothesisEvaluationReport:
    """
    Immutable report containing the complete outcome of one
    hypothesis evaluation cycle.

    This model is the public contract between the hypothesis
    evaluation layer and downstream consumers such as the
    StrategyRecommendationEngine.

    The report is informational only.

    It never:
    - executes trades
    - changes configuration
    - modifies hypotheses
    - uses AI
    """

    evaluations: list[HypothesisEvaluation]

    @property
    def total(self) -> int:
        return len(self.evaluations)

    @property
    def supported(self) -> int:
        return sum(
            evaluation.supported
            for evaluation in self.evaluations
        )

    @property
    def rejected(self) -> int:
        return sum(
            (
                evaluation.status == "REJECTED"
            )
            for evaluation in self.evaluations
        )

    @property
    def insufficient_data(self) -> int:
        return sum(
            (
                evaluation.status == "INSUFFICIENT_DATA"
            )
            for evaluation in self.evaluations
        )

    @property
    def support_ratio(self) -> float:
        if self.total == 0:
            return 0.0

        return round(
            self.supported / self.total,
            4,
        )