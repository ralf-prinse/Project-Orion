from __future__ import annotations

from models.strategy_idea import StrategyIdea
from models.strategy_recommendation import StrategyRecommendation


class StrategyIdeaBuilder:
    """
    Deterministically converts recommendations into strategy ideas.

    Responsibilities:
        - preserve intent
        - preserve priority
        - preserve rationale

    This builder never:
        - proposes parameter values
        - changes configuration
        - executes trades
        - performs AI reasoning
    """

    def build(
        self,
        recommendation: StrategyRecommendation,
        idea_id: str,
    ) -> StrategyIdea:

        return StrategyIdea(
            idea_id=idea_id,
            recommendation=recommendation,
            title=recommendation.title,
            description=recommendation.description,
            objective=self._objective(recommendation),
            expected_benefit=self._expected_benefit(recommendation),
            rationale=recommendation.rationale,
            priority=recommendation.priority,
        )

    def _objective(
        self,
        recommendation: StrategyRecommendation,
    ) -> str:
        return (
            f"Evaluate whether '{recommendation.title}' "
            "results in measurable performance improvement."
        )

    def _expected_benefit(
        self,
        recommendation: StrategyRecommendation,
    ) -> str:
        return (
            "Validate the recommendation through controlled "
            "paper trading or replay before any future "
            "configuration changes are considered."
        )