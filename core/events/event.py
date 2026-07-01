from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Event:
    """
    Base event model for Project Orion.

    Events are deterministic data carriers. They do not execute logic, they do
    not mutate application state and they do not decide how subscribers should
    react. The EventBus is responsible only for delivery.
    """

    name: str
    payload: dict[str, Any] = field(default_factory=dict)
