from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionState:
    """
    Runtime state of an open position.

    This object contains mutable state used by the
    PositionManager while a trade is open.

    No AI.
    No persistence logic.
    No business decisions.
    """

    symbol: str

    entry_price: float

    current_stop_loss: float

    highest_price: float

    current_price: float

    break_even_active: bool = False

    trailing_stop_active: bool = False

    target_1_hit: bool = False

    target_2_hit: bool = False

    target_3_hit: bool = False