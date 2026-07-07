from __future__ import annotations

from dataclasses import dataclass

from models.live_paper_trading_config import LivePaperTradingConfig


@dataclass(frozen=True)
class AutonomousPaperTradingConfig:
    """
    Configuration for an autonomous finite paper trading session.

    The runner executes multiple cycles while preserving one
    TradingSession.
    """

    live_config: LivePaperTradingConfig = LivePaperTradingConfig()

    cycles: int = 3

    sleep_seconds: float = 0.0

    stop_on_exception: bool = False

    print_cycle_summary: bool = True