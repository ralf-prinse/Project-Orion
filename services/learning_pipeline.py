from __future__ import annotations

from models.learning_pipeline_result import LearningPipelineResult
from models.performance_analysis_result import PerformanceAnalysisResult
from models.strategy_idea import StrategyIdea
from services.strategy_idea_builder import StrategyIdeaBuilder
from services.strategy_recommendation_engine import (
    StrategyRecommendationEngine,
)


class LearningPipeline:
    """
    Deterministic learning pipeline.

    Converts performance analysis into strategy ideas.

    The pipeline is informational only.

    It never:

    - changes trading configuration
    - executes trades
    - generates strategy variants
    - performs replay
    """

    def __init__(
        self,
        recommendation_engine: StrategyRecommendationEngine | None = None,
        idea_builder: StrategyIdeaBuilder | None = None,
    ):

        self._recommendation_engine = (
            recommendation_engine
            or StrategyRecommendationEngine()
        )

        self._idea_builder = (
            idea_builder
            or StrategyIdeaBuilder()
        )

    def run(
        self,
        performance: PerformanceAnalysisResult,
    ) -> LearningPipelineResult:

        recommendations = (
            self._recommendation_engine.build(
                performance,
            )
        )

        ideas: list[StrategyIdea] = []

        for index, recommendation in enumerate(
            recommendations.ordered,
            start=1,
        ):
            ideas.append(
                self._idea_builder.build(
                    recommendation,
                    idea_id=f"IDEA-{index:04d}",
                )
            )

        return LearningPipelineResult(
            performance=performance,
            recommendations=recommendations,
            ideas=tuple(ideas),
        )