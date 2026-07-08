from __future__ import annotations

from dataclasses import dataclass

from models.strategy_recommendation import StrategyRecommendation


@dataclass(frozen=True)
class StrategyIdea:
    """
    Immutable description of a deterministic improvement idea.

    A StrategyIdea captures the intent behind a recommendation without
    proposing concrete parameter values.

    It is an intermediate contract between recommendation generation
    and future controlled strategy experiments.

    A StrategyIdea never:
    - changes configuration
    - proposes parameter values
    - executes trades
    - uses AI
    """

    idea_id: str

    recommendation: StrategyRecommendation

    title: str

    description: str

    objective: str

    expected_benefit: str

    rationale: str

    priority: int

    @property
    def category(self) -> str:
        return self.recommendation.category