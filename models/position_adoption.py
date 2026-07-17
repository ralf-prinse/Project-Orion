from __future__ import annotations

from dataclasses import dataclass

from models.trading_session import TradingSession


@dataclass(frozen=True)
class PositionAdoptionRecord:
    symbol: str
    adopted: bool
    reason: str
    strategy: str


@dataclass(frozen=True)
class PositionAdoptionResult:
    session: TradingSession
    records: tuple[PositionAdoptionRecord, ...]


@dataclass(frozen=True)
class PositionAdoptionConfig:
    allowed_symbols: tuple[str, ...]
    strategy: str = "ORION_MANAGED_EXIT_V1"
