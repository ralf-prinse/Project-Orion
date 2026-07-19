from __future__ import annotations

from typing import Protocol

from models.completed_trade_record import CompletedTradeRecord


class CompletedTradeRepository(Protocol):
    def append_unique(self, record: CompletedTradeRecord) -> bool: ...

    def load_all(self) -> list[CompletedTradeRecord]: ...
