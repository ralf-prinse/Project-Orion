from __future__ import annotations

from dataclasses import dataclass
from math import floor


@dataclass(frozen=True)
class PositionSizingResult:
    symbol: str
    available_cash: float
    price: float
    shares: int
    investment: float
    remaining_cash: float
    is_affordable: bool


class PositionSizingService:
    """
    Deterministic position sizing service.

    Calculates how many whole shares fit within the available trading capital.

    This service does not create BUY / HOLD / SELL decisions.
    TradingPipeline remains the only source of trading decisions.
    """

    def calculate(
        self,
        symbol: str,
        available_cash: float,
        price: float,
    ) -> PositionSizingResult:
        normalized_symbol = str(symbol).strip().upper()
        cash = max(0.0, float(available_cash))
        share_price = max(0.0, float(price))

        if not normalized_symbol or cash <= 0 or share_price <= 0:
            return PositionSizingResult(
                symbol=normalized_symbol,
                available_cash=cash,
                price=share_price,
                shares=0,
                investment=0.0,
                remaining_cash=cash,
                is_affordable=False,
            )

        shares = floor(cash / share_price)
        investment = round(shares * share_price, 2)
        remaining_cash = round(cash - investment, 2)

        return PositionSizingResult(
            symbol=normalized_symbol,
            available_cash=round(cash, 2),
            price=round(share_price, 2),
            shares=shares,
            investment=investment,
            remaining_cash=remaining_cash,
            is_affordable=shares > 0,
        )