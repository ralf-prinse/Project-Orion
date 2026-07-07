from __future__ import annotations

from dataclasses import dataclass

from models.paper_trading_run_result import PaperTradingRunResult


@dataclass(frozen=True)
class PaperTradingDemoResult:
    """
    Immutable summary of a complete Paper Trading demo run.

    This model contains only presentation-independent information.
    """

    run: PaperTradingRunResult

    initial_cash: float
    final_cash: float
    final_equity: float

    total_cycles: int
    opened_positions: int
    closed_positions: int

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