from __future__ import annotations

from datetime import datetime

from models.execution_result import ExecutionResult
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.portfolio_snapshot import PortfolioSnapshot


class PortfolioManager:
    """
    Applies accepted broker-neutral execution results to a paper portfolio.

    This service performs deterministic portfolio calculations only.

    For Interactive Brokers runtimes, the resulting portfolio remains
    provisional until Broker Truth Synchronization replaces it with the
    authoritative broker state.

    No trading decisions.
    No broker-specific logic.
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
        side = order.side.strip().upper()

        total_value = (
            result.executed_price
            * result.executed_quantity
        )

        if side == "BUY":
            return self._apply_buy(
                portfolio=portfolio,
                symbol=order.symbol,
                quantity=result.executed_quantity,
                price=result.executed_price,
                total_cost=total_value,
            )

        if side == "SELL":
            return self._apply_sell(
                portfolio=portfolio,
                symbol=order.symbol,
                quantity=result.executed_quantity,
                total_proceeds=total_value,
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

        normalized_symbol = symbol.strip().upper()
        updated_positions = dict(portfolio.positions)

        updated_positions[normalized_symbol] = PaperPosition(
            symbol=normalized_symbol,
            quantity=quantity,
            entry_price=price,
            current_price=price,
        )

        return PaperPortfolio(
            cash=round(
                portfolio.cash - total_cost,
                2,
            ),
            positions=updated_positions,
        )

    def _apply_sell(
        self,
        portfolio: PaperPortfolio,
        symbol: str,
        quantity: int,
        total_proceeds: float,
    ) -> PaperPortfolio:

        normalized_symbol = symbol.strip().upper()
        position = portfolio.positions.get(normalized_symbol)

        # ExecutionValidator should already prevent this situation.
        # The guard keeps this service deterministic when called directly.
        if position is None:
            return portfolio

        if quantity <= 0:
            return portfolio

        if quantity > position.quantity:
            return portfolio

        updated_positions = dict(portfolio.positions)
        remaining_quantity = position.quantity - quantity

        if remaining_quantity == 0:
            del updated_positions[normalized_symbol]
        else:
            updated_positions[normalized_symbol] = PaperPosition(
                symbol=position.symbol,
                quantity=remaining_quantity,
                entry_price=position.entry_price,
                current_price=position.current_price,
            )

        return PaperPortfolio(
            cash=round(
                portfolio.cash + total_proceeds,
                2,
            ),
            positions=updated_positions,
        )