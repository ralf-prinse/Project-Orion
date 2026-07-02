from dataclasses import dataclass
from typing import List, Literal


MarketRegime = Literal["BULL", "BEAR", "SIDEWAYS"]
VolatilityState = Literal["LOW", "MEDIUM", "HIGH"]


@dataclass(frozen=True)
class IndicatorPack:
    """
    Raw output from analysis layer.
    """
    symbol: str
    rsi: float
    trend: float
    volatility: float
    momentum: float
    volume: float = 0.0


@dataclass(frozen=True)
class MarketIntelligenceSnapshot:
    """
    FINAL intelligence layer output.
    This is AI-ready.
    """

    symbol: str

    composite_score: float
    confidence: float

    regime: MarketRegime
    volatility_state: VolatilityState

    trend_strength: float
    momentum_strength: float
    risk_score: float

    ai_feature_vector: List[float]