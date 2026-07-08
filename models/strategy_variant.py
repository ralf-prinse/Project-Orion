from __future__ import annotations

from dataclasses import dataclass

from models.strategy_recommendation import StrategyRecommendation


@dataclass(frozen=True)
class StrategyVariantProposal:
    """
    Immutable proposal for a future strategy variant.

    A proposal represents one deterministic improvement idea derived
    from ORION's self-evaluation.

    A proposal is NOT a strategy configuration.

    It contains only the intent of the proposed change.
    """

    proposal_id: str

    recommendation: StrategyRecommendation

    parameter_name: str

    current_value: float

    proposed_value: float

    rationale: str

    expected_impact: float