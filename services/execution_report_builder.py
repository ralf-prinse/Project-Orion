from __future__ import annotations

from dataclasses import dataclass

from models.execution_context import ExecutionContext
from models.execution_result import ExecutionResult
from models.portfolio_snapshot import PortfolioSnapshot


@dataclass(frozen=True)
class ExecutionReport:
    """
    Human-readable deterministic execution report.

    No AI.
    No trading decisions.
    """

    symbol: str
    status: str
    message: str
    cash: float
    equity: float
    open_positions: int


class ExecutionReportBuilder:
    """
    Builds deterministic execution reports.
    """

    def build(
        self,
        context: ExecutionContext,
        result: ExecutionResult,
        snapshot: PortfolioSnapshot,
    ) -> ExecutionReport:

        return ExecutionReport(
            symbol=context.symbol,
            status=result.status,
            message=result.message,
            cash=snapshot.cash,
            equity=snapshot.equity,
            open_positions=snapshot.open_positions,
        )