from __future__ import annotations

from dataclasses import dataclass

from models.live_paper_trading_result import LivePaperTradingResult
from models.portfolio_allocation_result import PortfolioAllocationResult
from models.trading_session import TradingSession


@dataclass(frozen=True)
class AutonomousPaperTradingCycleResult:
    """
    Immutable result of one autonomous paper trading cycle.
    """

    scan: LivePaperTradingResult
    allocation: PortfolioAllocationResult

    executed_trades: int
    rejected_trades: int


@dataclass(frozen=True)
class AutonomousPaperTradingResult:
    """
    Immutable result of an autonomous multi-cycle paper trading session.
    """

    session: TradingSession

    cycle_results: list[AutonomousPaperTradingCycleResult]

    completed_cycles: int
    failed_cycles: int

    initial_cash: float
    final_cash: float
    final_equity: float

    @property
    def total_executed_trades(self) -> int:
        return sum(
            cycle.executed_trades
            for cycle in self.cycle_results
        )

    @property
    def total_rejected_trades(self) -> int:
        return sum(
            cycle.rejected_trades
            for cycle in self.cycle_results
        )

    @property
    def total_failed_symbols(self) -> int:
        return sum(
            cycle.scan.failed_symbols
            for cycle in self.cycle_results
        )

    @property
    def profit(self) -> float:
        return round(
            self.final_equity - self.initial_cash,
            2,
        )

    @property
    def return_percent(self) -> float:
        if self.initial_cash == 0:
            return 0.0

        return round(
            (self.profit / self.initial_cash) * 100,
            2,
        )