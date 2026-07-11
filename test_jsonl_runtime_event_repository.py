import json
from datetime import datetime
from tempfile import TemporaryDirectory
from pathlib import Path

from models.runtime_event import RuntimeEvent
from services.stores.jsonl_runtime_event_repository import (
    JsonlRuntimeEventRepository,
)


def test_repository_appends_jsonl_event():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "runtime" / "events.jsonl"
        repository = JsonlRuntimeEventRepository(path)
        repository.append(
            RuntimeEvent(
                timestamp=datetime(2026, 7, 11, 12, 0, 0),
                event_type="RUNTIME_STARTED",
                status="RUNNING",
                iteration=0,
                message="Started.",
            )
        )

        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        payload = json.loads(lines[0])
        assert payload["event_type"] == "RUNTIME_STARTED"
        assert payload["timestamp"] == "2026-07-11T12:00:00"
        assert payload["status"] == "RUNNING"


def main():
    test_repository_appends_jsonl_event()
    print("JSONL RUNTIME EVENT REPOSITORY: PASS")


if __name__ == "__main__":
    main()
