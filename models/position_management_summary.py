from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PositionManagementSummary:
    """
    Central deterministic summary for position management.

    This object bundles the output of all position-management
    services into one stable result object.

    No BUY.
    No SELL.
    No EXIT.
    No AI.
    No persistence.
    """

    symbol: str
    current_price: float
    stop_loss: float

    status: str
    score: int

    actions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    break_even: Any | None = None
    trailing_stop: Any | None = None
    time_stop: Any | None = None
    position_health: Any | None = None

    @property
    def has_actions(self) -> bool:
        return bool(self.actions)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)