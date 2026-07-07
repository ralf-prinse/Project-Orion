from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.trading_session import TradingSession


@dataclass(frozen=True)
class TradingCycleResult:
    """
    Result of one TradingCycle tick.
    """

    symbol: str
    session: TradingSession
    action: str
    message: str
    opened: Any | None = None
    updated: Any | None = None
    closed: Any | None = None