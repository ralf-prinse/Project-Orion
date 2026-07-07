from __future__ import annotations

from dataclasses import dataclass

from models.execution_request import ExecutionRequest
from models.paper_portfolio import PaperPortfolio


@dataclass(frozen=True)
class ExecutionContext:
    request: ExecutionRequest
    portfolio: PaperPortfolio
    trading_mode: str = "PAPER"
    max_position_percentage: float = 1.0
    allow_fractional_shares: bool = False

    @property
    def symbol(self) -> str:
        return self.request.symbol.upper()

    @property
    def available_cash(self) -> float:
        return round(self.portfolio.cash, 2)

    @property
    def portfolio_equity(self) -> float:
        return round(self.portfolio.equity, 2)

    @property
    def requested_value(self) -> float:
        return round(self.request.entry_price * self.request.quantity, 2)

    @property
    def position_size_percent(self) -> float:
        if self.portfolio_equity <= 0:
            return 0.0

        return round(self.requested_value / self.portfolio_equity, 4)