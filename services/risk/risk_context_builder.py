from __future__ import annotations

from models.risk_context import RiskContext
from services.intelligence.intelligence_models import (
    IndicatorPack,
    MarketIntelligenceSnapshot,
)


class RiskContextBuilder:
    """
    Converts pipeline outputs into a deterministic RiskContext.

    Single responsibility:
    Build the complete input for AdaptiveRiskEngine.
    """

    def build(
        self,
        indicator_pack: IndicatorPack,
        intelligence: MarketIntelligenceSnapshot,
        confidence: float,
    ) -> RiskContext:

        return RiskContext(
            symbol=indicator_pack.symbol,
            entry_price=indicator_pack.price,
            confidence=confidence,
            risk_score=intelligence.risk_score,
            regime=intelligence.regime,
            volatility=intelligence.volatility_state,
            market_structure=indicator_pack.market_structure,
        )