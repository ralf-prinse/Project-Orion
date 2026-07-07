from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyRecommendation:
    """
    One self-generated recommendation produced by ORION.

    Recommendations are informational only.
    They never modify trading behaviour directly.
    """

    title: str

    description: str

    priority: int

    confidence: float

    expected_impact: float

    category: str

    rationale: str


@dataclass(frozen=True)
class StrategyRecommendationResult:
    """
    Immutable collection of self-generated recommendations.
    """

    recommendations: list[StrategyRecommendation]

    @property
    def ordered(self) -> list[StrategyRecommendation]:
        return sorted(
            self.recommendations,
            key=lambda recommendation: (
                recommendation.priority,
                -recommendation.expected_impact,
            ),
        )