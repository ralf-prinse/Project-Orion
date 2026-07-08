from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from models.trade_journal_entry import TradeJournalEntry


class TradeJournalRepository(ABC):
    """
    Abstract repository for persistent trade journal storage.

    Implementations may use JSONL, SQLite, PostgreSQL or cloud storage.

    Trading and learning services should depend only on this contract.
    """

    @abstractmethod
    def append(
        self,
        entry: TradeJournalEntry,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_all(self) -> list[TradeJournalEntry]:
        raise NotImplementedError

    @abstractmethod
    def exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        raise NotImplementedError