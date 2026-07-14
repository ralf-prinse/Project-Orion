from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MarketSessionState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class MarketDefinition:
    """
    Definition of a regular exchange trading session.

    Opening and closing times are expressed in the exchange's
    own local timezone. DST conversion is delegated to zoneinfo.
    """

    code: str
    name: str
    timezone_name: str

    open_hour: int
    open_minute: int

    close_hour: int
    close_minute: int


@dataclass(frozen=True)
class MarketSessionStatus:
    """
    Current status of one market.

    All absolute timestamps are timezone-aware.
    """

    market: MarketDefinition
    state: MarketSessionState

    evaluated_at_utc: datetime
    local_time: datetime

    session_open: datetime | None
    session_close: datetime | None
    next_open: datetime

    reason: str

    @property
    def is_open(self) -> bool:
        return self.state is MarketSessionState.OPEN