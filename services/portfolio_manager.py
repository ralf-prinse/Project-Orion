from __future__ import annotations

from models.execution_result import ExecutionResult
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.portfolio_snapshot import PortfolioSnapshot
from datetime import datetime


class PortfolioManager:
    """
    Applies execution results to a paper portfolio.

    No trading decisions.
    No broker logic.
    No AI.
    """

    def apply_execution(
        self,
        portfolio: PaperPortfolio,
        result: ExecutionResult,
    ) -> PaperPortfolio:

        if not result.accepted or result.order is None:
            return portfolio

        order = result.order
        total_cost = result.executed_price * result.executed_quantity

        if order.side == "BUY":
            return self._apply_buy(
                portfolio=portfolio,
                symbol=order.symbol,
                quantity=result.executed_quantity,
                price=result.executed_price,
                total_cost=total_cost,
            )

        return portfolio

    def snapshot(
        self,
        portfolio: PaperPortfolio,
    ) -> PortfolioSnapshot:

        unrealized = sum(
            position.unrealized_profit_loss
            for position in portfolio.positions.values()
        )

        return PortfolioSnapshot(
            cash=round(portfolio.cash, 2),
            equity=portfolio.equity,
            positions_value=portfolio.positions_value,
            open_positions=len(portfolio.positions),
            realized_profit_loss=0.0,
            unrealized_profit_loss=round(unrealized, 2),
            created_at=datetime.now(),
        )

    def _apply_buy(
        self,
        portfolio: PaperPortfolio,
        symbol: str,
        quantity: int,
        price: float,
        total_cost: float,
    ) -> PaperPortfolio:

        updated_positions = dict(portfolio.positions)

        updated_positions[symbol.upper()] = PaperPosition(
            symbol=symbol.upper(),
            quantity=quantity,
            entry_price=price,
            current_price=price,
        )

        return PaperPortfolio(
            cash=round(portfolio.cash - total_cost, 2),
            positions=updated_positions,
        )