from __future__ import annotations

import json
from pathlib import Path

from models.news_event import NewsEvent
from services.serialization.dataclass_serializer import DataclassSerializer


class JsonlNewsEventRepository:
    def __init__(
        self,
        path: Path | str = "data/ibkr_news_events.jsonl",
        serializer: DataclassSerializer | None = None,
    ) -> None:
        self.path = Path(path)
        self.serializer = serializer or DataclassSerializer()
        self._known_ids: set[str] | None = None

    def append_unique(self, event: NewsEvent) -> bool:
        known_ids = self._load_known_ids()
        if event.event_id in known_ids:
            return False
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    self.serializer.to_dict(event),
                    ensure_ascii=False,
                )
                + "\n"
            )
        known_ids.add(event.event_id)
        return True

    def load_all(self) -> list[NewsEvent]:
        if not self.path.exists():
            return []
        return [
            self.serializer.from_dict(NewsEvent, json.loads(line))
            for line in self.path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def _load_known_ids(self) -> set[str]:
        if self._known_ids is None:
            self._known_ids = {
                event.event_id
                for event in self.load_all()
            }
        return self._known_ids
