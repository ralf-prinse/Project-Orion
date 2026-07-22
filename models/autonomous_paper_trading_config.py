from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from models.live_paper_trading_config import LivePaperTradingConfig


@dataclass(frozen=True)
class AutonomousPaperTradingConfig:
    """
    Configuration for an autonomous finite paper trading session.

    The runner executes multiple cycles while preserving one
    TradingSession.
    """

    EXIT_ONLY: ClassVar[str] = "EXIT_ONLY"
    BUY_AND_SELL: ClassVar[str] = "BUY_AND_SELL"
    SHADOW: ClassVar[str] = "SHADOW"

    live_config: LivePaperTradingConfig = LivePaperTradingConfig()

    execution_mode: str = BUY_AND_SELL

    cycles: int = 3

    sleep_seconds: float = 0.0

    stop_on_exception: bool = False

    print_cycle_summary: bool = True

    def __post_init__(self) -> None:
        normalized = self.execution_mode.strip().upper()

        if normalized not in {
            self.EXIT_ONLY,
            self.BUY_AND_SELL,
            self.SHADOW,
        }:
            raise ValueError(
                "execution_mode must be EXIT_ONLY or BUY_AND_SELL, "
                "or SHADOW."
            )

        object.__setattr__(self, "execution_mode", normalized)

        if (
            self.live_config.capital_profile
            == LivePaperTradingConfig.MICRO_500
            and normalized != self.SHADOW
        ):
            raise ValueError(
                "MICRO_500 capital profile is restricted to SHADOW mode."
            )

        if self.cycles < 1:
            raise ValueError("cycles must be at least 1.")

        if self.sleep_seconds < 0:
            raise ValueError("sleep_seconds must not be negative.")
