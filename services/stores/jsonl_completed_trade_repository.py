from __future__ import annotations

import json
from pathlib import Path

from models.completed_trade_record import CompletedTradeRecord
from services.serialization.dataclass_serializer import DataclassSerializer


class JsonlCompletedTradeRepository:
    """Append-only store with trade_id based idempotency."""

    def __init__(self, path: Path | str, serializer=None) -> None:
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()

    def append_unique(self, record: CompletedTradeRecord) -> bool:
        if any(item.trade_id == record.trade_id for item in self.load_all()):
            return False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    self.serializer.to_dict(record),
                    ensure_ascii=False,
                )
                + "\n"
            )
        return True

    def load_all(self) -> list[CompletedTradeRecord]:
        if not self.path.exists():
            return []
        return [
            self.serializer.from_dict(CompletedTradeRecord, json.loads(line))
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
