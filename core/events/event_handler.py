from __future__ import annotations

from typing import Protocol, runtime_checkable

from core.events.event import Event


@runtime_checkable
class EventHandler(Protocol):
    """
    Protocol for synchronous Orion event handlers.

    Handlers should remain lightweight and deterministic. Long-running work,
    external API calls and asynchronous dispatch are intentionally outside the
    scope of the Event Bus foundation.
    """

    def __call__(self, event: Event) -> None:
        """Handle one published event."""
