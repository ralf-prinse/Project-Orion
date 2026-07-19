from __future__ import annotations

from dataclasses import dataclass, field

from models.hypothesis_evaluation_report import HypothesisEvaluationReport
from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_recommendation import StrategyRecommendationResult
from models.strategy_variant import StrategyVariantProposal


@dataclass(frozen=True)
class LearningCycleResult:
    """
    Immutable result of one controlled learning cycle.

    This result is informational only.

    It never:
    - changes trading configuration
    - executes trades
    - modifies hypotheses
    - enables auto-tuning
    """

    performance: PerformanceAnalysisResult

    hypothesis_report: HypothesisEvaluationReport

    recommendations: StrategyRecommendationResult

    proposals: list[StrategyVariantProposal] = field(default_factory=list)

    @property
    def proposal_count(self) -> int:
        return len(self.proposals)

    @property
    def has_actionable_proposals(self) -> bool:
        return self.proposal_count > 0
