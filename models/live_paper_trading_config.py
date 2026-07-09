from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LivePaperTradingConfig:
    """
    Configuration for live paper trading.

    Uses real market data, but only paper money.
    """

    watchlist_path: Path = Path("data/universes/swing.csv")

    initial_cash: float = 500.0

    max_symbols: int = 250

    max_open_positions: int = 50

    min_confidence: float = 0.75

    max_position_value: float = 150.0

    max_position_size_pct: float = 0.10

    max_portfolio_exposure: float = 0.95

    min_cash_reserve_pct: float = 0.05

    history_period: str = "3mo"
    history_interval: str = "1d"

    allow_fractional_shares: bool = False

    take_profit_percent: float = 0.08
    stop_loss_percent: float = 0.04
    trailing_stop_percent: float = 0.03
    break_even_trigger_percent: float = 0.05
    max_holding_days: int = 20

    enable_trailing_stop: bool = True
    enable_break_even: bool = True