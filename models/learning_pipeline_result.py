from __future__ import annotations

from dataclasses import dataclass, field

from models.performance_analysis_result import (
    PerformanceAnalysisResult,
)
from models.strategy_idea import StrategyIdea
from models.strategy_recommendation import (
    StrategyRecommendationResult,
)


@dataclass(frozen=True)
class LearningPipelineResult:
    """
    Immutable result produced by one LearningPipeline execution.

    The Learning Pipeline is deterministic and informational only.

    It never:
        - changes configuration
        - executes trades
        - creates strategy variants
        - performs replay testing
        - performs AI reasoning
    """

    performance: PerformanceAnalysisResult

    recommendations: StrategyRecommendationResult

    ideas: tuple[StrategyIdea, ...] = field(
        default_factory=tuple,
    )

    @property
    def idea_count(self) -> int:
        return len(self.ideas)

    @property
    def has_ideas(self) -> bool:
        return self.idea_count > 0