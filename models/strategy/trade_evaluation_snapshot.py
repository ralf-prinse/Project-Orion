from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(slots=True)
class TradeEvaluationSnapshot:
    """
    Complete momentopname van een trade.

    Deze snapshot wordt opgeslagen:

    - bij ENTRY
    - tijdens POSITION REVIEW
    - bij EXIT

    De snapshot verandert GEEN gedrag van Orion.

    Hij wordt uitsluitend gebruikt
    voor analyse en toekomstige learning.
    """

    symbol: str

    timestamp: datetime

    phase: str

    conviction: float

    opportunity_score: float

    thesis: str

    market_regime: str

    trend_score: float

    momentum_score: float

    volume_score: float

    volatility_score: float

    risk_reward: float

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    notes: str = ""