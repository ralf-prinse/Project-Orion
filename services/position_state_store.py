from __future__ import annotations

from models.position_state import PositionState


class PositionStateStore:
    """
    In-memory runtime store for PositionState objects.

    No trading decisions.
    No order execution.
    No UI.
    """

    def __init__(self):
        self._states: dict[str, PositionState] = {}

    def save(
        self,
        state: PositionState,
    ) -> None:
        self._states[state.symbol.upper()] = state

    def load(
        self,
        symbol: str,
    ) -> PositionState | None:
        return self._states.get(
            str(symbol).strip().upper()
        )

    def load_all(self) -> list[PositionState]:
        return list(self._states.values())

    def remove(
        self,
        symbol: str,
    ) -> None:
        self._states.pop(
            str(symbol).strip().upper(),
            None,
        )

    def clear(self) -> None:
        self._states.clear()