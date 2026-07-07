from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LivePaperTradingConfig:
    """
    Configuration for live paper trading.

    Uses real market data, but only paper money.
    """

    watchlist_path: Path = Path("config/watchlist.txt")

    initial_cash: float = 500.0

    max_symbols: int = 25
    max_open_positions: int = 3

    min_confidence: float = 0.75
    max_position_value: float = 150.0

    history_period: str = "3mo"
    history_interval: str = "1d"

    allow_fractional_shares: bool = False