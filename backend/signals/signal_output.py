from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SignalType(str, Enum):
    """
    Deterministic trading signal.

    Generated exclusively by the TradingPipeline.
    """

    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    EXIT = "EXIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    STOP_LOSS = "STOP_LOSS"
    TRAILING_STOP = "TRAILING_STOP"
    AVOID = "AVOID"


@dataclass(frozen=True)
class SignalOutput:
    """
    Deterministic trading signal produced by Orion.

    This model is the single presentation contract between the
    deterministic backend and all UI layers.

    AI never modifies this model.
    AI only explains its contents.
    """

    symbol: str

    signal: SignalType

    confidence: float
    risk_score: float

    entry_price: float
    current_price: float

    target_price: float
    stop_loss: float

    position_size: int

    expected_profit_per_share: float
    expected_loss_per_share: float

    risk_reward_ratio: float

    timeframe: str = "Intraday"

    timestamp: datetime = field(default_factory=datetime.utcnow)

    reason_codes: tuple[str, ...] = field(default_factory=tuple)

    metadata: dict = field(default_factory=dict)

    @property
    def expected_total_profit(self) -> float:
        return self.expected_profit_per_share * self.position_size

    @property
    def expected_total_loss(self) -> float:
        return self.expected_loss_per_share * self.position_size

    @property
    def is_entry_signal(self) -> bool:
        return self.signal == SignalType.BUY

    @property
    def is_exit_signal(self) -> bool:
        return self.signal in (
            SignalType.SELL,
            SignalType.EXIT,
            SignalType.TAKE_PROFIT,
            SignalType.STOP_LOSS,
            SignalType.TRAILING_STOP,
        )