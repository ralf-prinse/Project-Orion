from dataclasses import dataclass
from typing import Literal


DecisionType = Literal["BUY", "SELL", "HOLD"]


@dataclass(frozen=True)
class MarketSignal:
    """
    Clean normalized signal used by decision engines.

    score: 0.0 - 1.0
    trend: -1.0 - 1.0
    volatility: 0.0 - 1.0
    momentum: 0.0 - 1.0
    """

    symbol: str
    score: float
    trend: float
    volatility: float
    momentum: float


@dataclass(frozen=True)
class PositionContext:
    """
    Portfolio context used for sizing and risk calculations.
    """

    cash: float
    position_size: float = 0.0
    exposure: float = 0.0
    max_position_percentage: float = 1.0


@dataclass(frozen=True)
class DecisionInput:
    """
    Explicit input object for decision and sizing logic.
    """

    signal: MarketSignal
    context: PositionContext


@dataclass(frozen=True)
class TradeDecision:
    """
    Pure decision result.

    Position sizing is handled separately by PositionSizer.
    """

    symbol: str
    decision: DecisionType
    confidence: float
    reason: str


@dataclass(frozen=True)
class SizedTradeDecision:
    """
    Final execution-ready decision after sizing.
    """

    symbol: str
    decision: DecisionType
    confidence: float
    reason: str
    position_size: float
    expected_risk: float