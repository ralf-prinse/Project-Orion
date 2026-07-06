from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskPlan:
    """
    Adaptive Risk Engine output.

    This object contains the complete trading plan
    generated for a BUY opportunity.

    It contains no business logic and is immutable.
    """

    symbol: str

    entry_price: float

    stop_loss: float

    target_1: float

    target_2: float

    target_3: float

    risk_percent: float

    reward_percent: float

    risk_reward_ratio: float

    confidence: float

    notes: str = ""