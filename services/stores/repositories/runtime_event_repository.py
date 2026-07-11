from __future__ import annotations

from typing import Protocol

from models.runtime_event import RuntimeEvent


class RuntimeEventRepository(Protocol):
    def append(self, event: RuntimeEvent) -> None:
        """Persist one operational runtime event."""
