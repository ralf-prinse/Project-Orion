from __future__ import annotations

from dataclasses import dataclass

from models.paper_portfolio import PaperPortfolio
from services.position_monitor import PositionMonitorResult


@dataclass(frozen=True)
class ExitExecutionResult:
    symbol: str
    executed: bool
    action: str
    reason: str


class ExitEngine:
    """
    Executes exit decisions produced by the PositionMonitor.

    This service is intentionally isolated from market analysis.
    It only applies an already-made exit decision to the portfolio.
    """

    SELL_ACTIONS = {
        "TAKE_PROFIT",
        "STOP_LOSS",
        "MAX_HOLDING_TIME",
    }

    def execute(
        self,
        portfolio: PaperPortfolio,
        decision: PositionMonitorResult,
    ) -> ExitExecutionResult:
        if decision.action not in self.SELL_ACTIONS:
            return ExitExecutionResult(
                symbol=decision.symbol,
                executed=False,
                action=decision.action,
                reason="No exit execution required.",
            )

        if decision.symbol not in portfolio.positions:
            return ExitExecutionResult(
                symbol=decision.symbol,
                executed=False,
                action=decision.action,
                reason="Position not found.",
            )

        position = portfolio.positions.pop(decision.symbol)

        proceeds = (
            position.quantity
            * decision.current_price
        )

        portfolio.cash = round(
            portfolio.cash + proceeds,
            2,
        )

        return ExitExecutionResult(
            symbol=decision.symbol,
            executed=True,
            action=decision.action,
            reason=f"Position closed ({decision.action}).",
        )