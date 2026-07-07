from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketSnapshot:
    """
    One deterministic market update for one symbol.

    No trading decisions.
    No AI.
    """

    symbol: str
    current_price: float
    pipeline_output: dict | None = None