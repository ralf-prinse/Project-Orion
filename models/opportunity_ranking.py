from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OpportunityRankFactor:
    name: str
    score: float
    weight: float
    contribution: float
    rationale: str


@dataclass(frozen=True)
class OpportunityRanking:
    symbol: str
    score: float
    rank_band: str
    factors: tuple[OpportunityRankFactor, ...]
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]
    summary: str
