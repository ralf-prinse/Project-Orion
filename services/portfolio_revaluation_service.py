from __future__ import annotations

from dataclasses import replace

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition


class PortfolioRevaluationService:
    """
    Updates current prices for open paper positions.

    This service only revalues existing positions.
    It does not create or close positions.
    """

    def revalue(
        self,
        portfolio: PaperPortfolio,
        prices: dict[str, float],
    ) -> PaperPortfolio:
        updated_positions: dict[str, PaperPosition] = {}

        for symbol, position in portfolio.positions.items():
            current_price = prices.get(symbol)

            if current_price is None:
                updated_positions[symbol] = position
                continue

            updated_positions[symbol] = replace(
                position,
                current_price=float(current_price),
            )

        return PaperPortfolio(
            cash=portfolio.cash,
            positions=updated_positions,
        )