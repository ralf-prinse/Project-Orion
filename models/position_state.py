from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class PositionState:
    """
    Runtime state of an open position.

    TradingSession owns this state for the complete
    lifetime of a managed paper position.

    No AI.
    No persistence logic.
    No trade execution.
    """

    symbol: str

    entry_price: float

    current_stop_loss: float

    highest_price: float

    current_price: float

    trade_id: str = ""

    break_even_active: bool = False

    trailing_stop_active: bool = False

    target_1_hit: bool = False

    target_2_hit: bool = False

    target_3_hit: bool = False

    opened_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
