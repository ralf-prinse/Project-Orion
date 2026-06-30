"""
Central configuration for Analysis Layer score weights.

These weights determine how much each specialised analyzer contributes
to the overall technical score.

MarketRegimeAnalyzer is intentionally excluded because it provides
market context rather than technical quality.
"""

TREND_WEIGHT = 0.25
MOMENTUM_WEIGHT = 0.20
VOLATILITY_WEIGHT = 0.15
STRUCTURE_WEIGHT = 0.15
VOLUME_WEIGHT = 0.15
RELATIVE_STRENGTH_WEIGHT = 0.10


ALL_WEIGHTS = {
    "trend": TREND_WEIGHT,
    "momentum": MOMENTUM_WEIGHT,
    "volatility": VOLATILITY_WEIGHT,
    "structure": STRUCTURE_WEIGHT,
    "volume": VOLUME_WEIGHT,
    "relative_strength": RELATIVE_STRENGTH_WEIGHT,
}