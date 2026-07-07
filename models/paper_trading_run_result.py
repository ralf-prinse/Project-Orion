from __future__ import annotations

from dataclasses import dataclass

from models.trading_cycle_result import TradingCycleResult
from models.trading_session import TradingSession


@dataclass(frozen=True)
class PaperTradingRunResult:
    """
    Result of a multi-cycle paper trading run.
    """

    session: TradingSession
    cycles: list[TradingCycleResult]

    @property
    def total_cycles(self) -> int:
        return len(self.cycles)

    @property
    def opened_positions(self) -> int:
        return len(
            [
                cycle
                for cycle in self.cycles
                if cycle.action == "OPEN_POSITION"
            ]
        )

    @property
    def closed_positions(self) -> int:
        return len(
            [
                cycle
                for cycle in self.cycles
                if cycle.action == "CLOSE_POSITION"
            ]
        )