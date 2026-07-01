from __future__ import annotations

from collections.abc import Callable

from core.events.event import Event
from core.events.event_registry import EventRegistry

EventHandlerCallable = Callable[[Event], None]


class EventBus:
    """
    Synchronous deterministic event bus for Project Orion.

    The first implementation is deliberately small: publish, subscribe and
    unsubscribe. It is designed for scan progress, logging, diagnostics,
    metrics and future GUI updates without coupling those listeners directly to
    orchestration code.
    """

    def __init__(self, registry: EventRegistry | None = None) -> None:
        self.registry = registry or EventRegistry()
        self._published_events: list[Event] = []

    def subscribe(
        self,
        event_type: type[Event],
        handler: EventHandlerCallable,
    ) -> None:
        self.registry.subscribe(event_type, handler)

    def unsubscribe(
        self,
        event_type: type[Event],
        handler: EventHandlerCallable,
    ) -> None:
        self.registry.unsubscribe(event_type, handler)

    def publish(self, event: Event) -> None:
        if not isinstance(event, Event):
            raise TypeError("Published object must be an Event instance.")

        self._published_events.append(event)

        for handler in self.registry.handlers_for(event):
            handler(event)

    def published_events(self) -> list[Event]:
        """
        Return published events in deterministic order.

        This method is primarily useful for tests and diagnostics. Production
        listeners should subscribe explicitly instead of polling this history.
        """

        return list(self._published_events)

    def clear_history(self) -> None:
        self._published_events.clear()
