from dataclasses import dataclass
from typing import Literal


DecisionType = Literal["BUY", "SELL", "HOLD"]


@dataclass(frozen=True)
class MarketSignal:
    symbol: str
    score: float
    trend: float
    volatility: float
    momentum: float


@dataclass(frozen=True)
class PositionContext:
    cash: float
    position_size: float = 0.0
    exposure: float = 0.0
    max_position_percentage: float = 1.0


@dataclass(frozen=True)
class DecisionInput:
    signal: MarketSignal
    context: PositionContext


@dataclass(frozen=True)
class TradeDecision:
    symbol: str
    decision: DecisionType
    confidence: float
    reason: str


@dataclass(frozen=True)
class SizedTradeDecision:
    symbol: str
    decision: DecisionType
    confidence: float
    reason: str
    position_size: float
    expected_risk: float
