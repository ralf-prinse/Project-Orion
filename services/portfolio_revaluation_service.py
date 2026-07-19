from __future__ import annotations

from dataclasses import replace

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.quote_validation_service import (
    QuoteValidationService,
)


class PortfolioRevaluationService:
    """
    Revalues existing paper positions.

    Missing or invalid quotes are ignored per symbol. The last valid
    price is retained, so one malformed provider value cannot poison
    portfolio equity.
    """

    def __init__(
        self,
        quote_validation_service: (
            QuoteValidationService | None
        ) = None,
    ):
        self.quote_validation_service = (
            quote_validation_service
            or QuoteValidationService()
        )

    def revalue(
        self,
        portfolio: PaperPortfolio,
        prices: dict[str, object],
    ) -> PaperPortfolio:
        updated_positions: dict[
            str,
            PaperPosition,
        ] = {}

        for symbol, position in (
            portfolio.positions.items()
        ):
            raw_price = prices.get(symbol)

            if raw_price is None:
                updated_positions[symbol] = (
                    position
                )
                continue

            validation = (
                self.quote_validation_service
                .validate(
                    symbol=symbol,
                    value=raw_price,
                )
            )

            if (
                not validation.valid
                or validation.normalized_price
                is None
            ):
                updated_positions[symbol] = (
                    position
                )
                continue

            updated_positions[symbol] = replace(
                position,
                current_price=(
                    validation.normalized_price
                ),
            )

        return PaperPortfolio(
            cash=portfolio.cash,
            positions=updated_positions,
            base_currency=portfolio.base_currency,
        )
