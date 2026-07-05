from __future__ import annotations

from dataclasses import dataclass
from math import floor

from services.market.fx_rate_service import FxRateService


@dataclass(frozen=True)
class PositionSizingResult:
    symbol: str

    account_currency: str
    market_currency: str

    available_cash: float
    available_market_cash: float

    price: float
    shares: int

    investment: float
    investment_market: float

    remaining_cash: float
    remaining_market_cash: float

    fx_rate: float
    fx_source: str

    is_affordable: bool


class PositionSizingService:
    """
    Deterministic position sizing service.

    Calculates how many whole shares fit within the available trading capital.

    Currency model
    --------------
    - available_cash is in account currency, usually EUR
    - price is in market currency, usually USD for US equities
    - FX conversion is delegated to FxRateService

    This service does not create BUY / HOLD / SELL decisions.
    TradingPipeline remains the only source of trading decisions.
    """

    def __init__(
        self,
        fx_rate_service: FxRateService | None = None,
    ) -> None:
        self._fx_rate_service = fx_rate_service or FxRateService()

    def calculate(
        self,
        symbol: str,
        available_cash: float,
        price: float,
        account_currency: str = "EUR",
        market_currency: str = "USD",
    ) -> PositionSizingResult:
        normalized_symbol = str(symbol).strip().upper()
        normalized_account_currency = str(account_currency).strip().upper()
        normalized_market_currency = str(market_currency).strip().upper()

        cash = max(0.0, float(available_cash))
        share_price = max(0.0, float(price))

        fx_rate = self._fx_rate_service.get_rate(
            from_currency=normalized_account_currency,
            to_currency=normalized_market_currency,
        )

        available_market_cash = round(cash * fx_rate.rate, 2)

        if not normalized_symbol or cash <= 0 or share_price <= 0:
            return PositionSizingResult(
                symbol=normalized_symbol,
                account_currency=normalized_account_currency,
                market_currency=normalized_market_currency,
                available_cash=round(cash, 2),
                available_market_cash=available_market_cash,
                price=round(share_price, 2),
                shares=0,
                investment=0.0,
                investment_market=0.0,
                remaining_cash=round(cash, 2),
                remaining_market_cash=available_market_cash,
                fx_rate=fx_rate.rate,
                fx_source=fx_rate.source,
                is_affordable=False,
            )

        shares = floor(available_market_cash / share_price)

        investment_market = round(shares * share_price, 2)
        remaining_market_cash = round(available_market_cash - investment_market, 2)

        if fx_rate.rate > 0:
            investment = round(investment_market / fx_rate.rate, 2)
            remaining_cash = round(remaining_market_cash / fx_rate.rate, 2)
        else:
            investment = 0.0
            remaining_cash = round(cash, 2)

        return PositionSizingResult(
            symbol=normalized_symbol,
            account_currency=normalized_account_currency,
            market_currency=normalized_market_currency,
            available_cash=round(cash, 2),
            available_market_cash=available_market_cash,
            price=round(share_price, 2),
            shares=shares,
            investment=investment,
            investment_market=investment_market,
            remaining_cash=remaining_cash,
            remaining_market_cash=remaining_market_cash,
            fx_rate=fx_rate.rate,
            fx_source=fx_rate.source,
            is_affordable=shares > 0,
        )