from __future__ import annotations

from dataclasses import dataclass

from models.market_structure import MarketStructure
from services.intelligence.intelligence_models import (
    MarketRegime,
    VolatilityState,
)


@dataclass(frozen=True)
class RiskContext:
    """
    Complete deterministic input for AdaptiveRiskEngine.

    This object contains everything required to build a RiskPlan.

    No business logic.
    No AI.
    No persistence.
    """

    symbol: str

    entry_price: float

    confidence: float

    risk_score: float

    regime: MarketRegime

    volatility: VolatilityState

    market_structure: MarketStructure