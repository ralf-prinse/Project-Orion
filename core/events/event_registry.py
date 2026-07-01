from __future__ import annotations

from collections.abc import Callable

from core.events.event import Event

EventHandlerCallable = Callable[[Event], None]


class EventRegistry:
    """
    Explicit synchronous event-handler registry.

    The registry maps event classes to ordered handler lists. Handler execution
    order is deterministic and follows subscription order. No auto-discovery or
    reflection is used.
    """

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandlerCallable]] = {}

    def subscribe(
        self,
        event_type: type[Event],
        handler: EventHandlerCallable,
    ) -> None:
        self._validate_event_type(event_type)
        self._validate_handler(handler)

        handlers = self._handlers.setdefault(event_type, [])

        if handler not in handlers:
            handlers.append(handler)

    def unsubscribe(
        self,
        event_type: type[Event],
        handler: EventHandlerCallable,
    ) -> None:
        self._validate_event_type(event_type)

        handlers = self._handlers.get(event_type, [])

        if handler in handlers:
            handlers.remove(handler)

        if not handlers and event_type in self._handlers:
            self._handlers.pop(event_type)

    def handlers_for(self, event: Event) -> list[EventHandlerCallable]:
        return list(self._handlers.get(type(event), []))

    def handler_count(self, event_type: type[Event]) -> int:
        self._validate_event_type(event_type)
        return len(self._handlers.get(event_type, []))

    def clear(self) -> None:
        self._handlers.clear()

    def _validate_event_type(self, event_type: type[Event]) -> None:
        if not isinstance(event_type, type) or not issubclass(event_type, Event):
            raise TypeError("event_type must be an Event subclass.")

    def _validate_handler(self, handler: EventHandlerCallable) -> None:
        if not callable(handler):
            raise TypeError("Event handler must be callable.")
