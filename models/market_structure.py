from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketStructure:
    """
    Deterministic market-structure data used by risk engines.

    No decisions.
    No AI.
    No persistence.
    """

    atr: float = 0.0
    average_range: float = 0.0

    swing_high: float = 0.0
    swing_low: float = 0.0

    resistance: float = 0.0
    support: float = 0.0