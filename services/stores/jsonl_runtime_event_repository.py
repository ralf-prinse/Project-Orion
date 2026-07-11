from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from models.runtime_event import RuntimeEvent


class JsonlRuntimeEventRepository:
    def __init__(self, path: Path | str):
        self.path = Path(path)

    def append(self, event: RuntimeEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(event)
        payload["timestamp"] = event.timestamp.isoformat()

        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False))
            handle.write("\n")
