from __future__ import annotations

import json
from pathlib import Path

from models.trade_journal_entry import TradeJournalEntry
from services.serialization.dataclass_serializer import (
    DataclassSerializer,
)
from services.stores.repositories.trade_journal_repository import (
    TradeJournalRepository,
)


class JsonlTradeJournalRepository(TradeJournalRepository):
    """
    JSONL implementation of TradeJournalRepository.

    Stores one TradeJournalEntry per line.
    This format is append-friendly and suitable for long-running paper
    trading sessions.
    """

    def __init__(
        self,
        path: Path | str = "data/trade_journal.jsonl",
        serializer: DataclassSerializer | None = None,
    ):
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()

    def append(
        self,
        entry: TradeJournalEntry,
    ) -> None:
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = self.serializer.to_dict(entry)

        with self.path.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                )
                + "\n"
            )

    def load_all(self) -> list[TradeJournalEntry]:
        if not self.exists():
            return []

        entries: list[TradeJournalEntry] = []

        for line in self.path.read_text(
            encoding="utf-8",
        ).splitlines():
            if not line.strip():
                continue

            entries.append(
                self.serializer.from_dict(
                    TradeJournalEntry,
                    json.loads(line),
                )
            )

        return entries

    def exists(self) -> bool:
        return self.path.exists()

    def delete(self) -> None:
        if self.exists():
            self.path.unlink()