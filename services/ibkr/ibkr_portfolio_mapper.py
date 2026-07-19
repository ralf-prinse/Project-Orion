from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

from models.broker_account import BrokerAccount
from models.broker_position import BrokerPosition
from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from services.market.fx_rate_service import FxRateService


class IbkrPortfolioMappingError(ValueError):
    """
    Raised when broker state cannot be mapped safely to an Orion portfolio.
    """


class IbkrPortfolioMapper:
    """
    Maps read-only IBKR broker state to the existing Orion PaperPortfolio.

    This mapper does not own lifecycle state, risk plans, exits or trading
    decisions. It only creates a deterministic portfolio snapshot from:

    - BrokerAccount
    - BrokerPosition records
    - externally validated current prices
    """

    SUPPORTED_BROKER_NAME = "IBKR"
    SUPPORTED_SECURITY_TYPE = "STK"
    ACTIVE_STATUS = "ACTIVE"

    def __init__(
        self,
        *,
        base_currency: str = "EUR",
        fx_rate_service: FxRateService | None = None,
        require_live_fx: bool = False,
    ) -> None:
        self._base_currency = base_currency.strip().upper()
        self._fx_rate_service = fx_rate_service or FxRateService()
        self._require_live_fx = bool(require_live_fx)

        if self._base_currency != "EUR":
            raise ValueError("IBKR Paper base currency must be EUR.")

    def map(
        self,
        *,
        account: BrokerAccount,
        positions: Sequence[BrokerPosition],
        current_prices: Mapping[str, float],
    ) -> PaperPortfolio:
        self._validate_account(account)

        normalized_prices = self._normalize_prices(
            current_prices
        )

        mapped_positions: dict[str, PaperPosition] = {}

        for broker_position in positions:
            paper_position = self._map_position(
                account=account,
                position=broker_position,
                current_prices=normalized_prices,
            )

            symbol = paper_position.symbol

            if symbol in mapped_positions:
                raise IbkrPortfolioMappingError(
                    "IBKR returned duplicate broker positions for "
                    f"symbol {symbol}."
                )

            mapped_positions[symbol] = paper_position

        return PaperPortfolio(
            cash=round(float(account.cash), 2),
            positions=mapped_positions,
            base_currency=self._base_currency,
        )

    def _validate_account(
        self,
        account: BrokerAccount,
    ) -> None:
        broker_name = account.broker_name.strip().upper()
        account_id = account.account_id.strip().upper()
        currency = account.currency.strip().upper()
        status = account.status.strip().upper()

        if broker_name != self.SUPPORTED_BROKER_NAME:
            raise IbkrPortfolioMappingError(
                "IbkrPortfolioMapper accepts only IBKR accounts."
            )

        if not account_id.startswith("DU"):
            raise IbkrPortfolioMappingError(
                "IBKR account ID must identify a Paper account "
                "starting with 'DU'."
            )

        if status != self.ACTIVE_STATUS:
            raise IbkrPortfolioMappingError(
                "IBKR account must be ACTIVE before portfolio mapping."
            )

        if not currency:
            raise IbkrPortfolioMappingError(
                "IBKR account currency must not be empty."
            )

        if currency != self._base_currency:
            raise IbkrPortfolioMappingError(
                "IBKR Paper account base currency must be EUR. "
                f"Received {currency}."
            )

        self._require_finite_non_negative(
            value=account.cash,
            field_name="IBKR account cash",
        )

        self._require_finite_non_negative(
            value=account.buying_power,
            field_name="IBKR account buying power",
        )

    def _normalize_prices(
        self,
        current_prices: Mapping[str, float],
    ) -> dict[str, float]:
        normalized: dict[str, float] = {}

        for raw_symbol, raw_price in current_prices.items():
            symbol = str(raw_symbol).strip().upper()

            if not symbol:
                raise IbkrPortfolioMappingError(
                    "Current-price symbols must not be empty."
                )

            if symbol in normalized:
                raise IbkrPortfolioMappingError(
                    "Duplicate current price supplied for "
                    f"symbol {symbol}."
                )

            price = self._require_finite_positive(
                value=raw_price,
                field_name=(
                    f"Current price for {symbol}"
                ),
            )

            normalized[symbol] = price

        return normalized

    def _map_position(
        self,
        *,
        account: BrokerAccount,
        position: BrokerPosition,
        current_prices: Mapping[str, float],
    ) -> PaperPosition:
        account_id = position.account_id.strip().upper()
        expected_account_id = account.account_id.strip().upper()
        symbol = position.symbol.strip().upper()
        security_type = position.security_type.strip().upper()
        currency = position.currency.strip().upper()

        if account_id != expected_account_id:
            raise IbkrPortfolioMappingError(
                "IBKR position belongs to unexpected account "
                f"{account_id or '<empty>'}."
            )

        if not symbol:
            raise IbkrPortfolioMappingError(
                "IBKR position symbol must not be empty."
            )

        if security_type != self.SUPPORTED_SECURITY_TYPE:
            raise IbkrPortfolioMappingError(
                "IbkrPortfolioMapper currently supports only "
                f"STK positions. Received {security_type or '<empty>'} "
                f"for {symbol}."
            )

        if not currency:
            raise IbkrPortfolioMappingError(
                f"IBKR position currency is missing for {symbol}."
            )

        quantity = self._require_whole_positive_quantity(
            position.quantity,
            symbol=symbol,
        )

        average_cost = self._require_finite_positive(
            value=position.average_cost,
            field_name=f"Average cost for {symbol}",
        )

        if symbol not in current_prices:
            raise IbkrPortfolioMappingError(
                "No validated current price was supplied for "
                f"IBKR position {symbol}."
            )

        current_price = current_prices[symbol]
        fx_rate = self._fx_rate_service.get_rate(
            currency,
            self._base_currency,
        )

        if self._require_live_fx and fx_rate.source == "fallback":
            raise IbkrPortfolioMappingError(
                f"Validated FX rate unavailable for {currency}/"
                f"{self._base_currency}; portfolio sync failed closed."
            )

        rate = self._require_finite_positive(
            value=fx_rate.rate,
            field_name=(
                f"FX rate for {currency}/{self._base_currency}"
            ),
        )

        return PaperPosition(
            symbol=symbol,
            quantity=quantity,
            entry_price=average_cost,
            current_price=current_price,
            currency=currency,
            fx_rate_to_base=rate,
        )

    def _require_whole_positive_quantity(
        self,
        value: float,
        *,
        symbol: str,
    ) -> int:
        try:
            quantity = float(value)
        except (TypeError, ValueError) as exc:
            raise IbkrPortfolioMappingError(
                f"Quantity for {symbol} must be numeric."
            ) from exc

        if not math.isfinite(quantity):
            raise IbkrPortfolioMappingError(
                f"Quantity for {symbol} must be finite."
            )

        if quantity <= 0:
            raise IbkrPortfolioMappingError(
                f"Quantity for {symbol} must be greater than zero."
            )

        if not quantity.is_integer():
            raise IbkrPortfolioMappingError(
                f"Quantity for {symbol} must be a whole number."
            )

        return int(quantity)

    def _require_finite_positive(
        self,
        *,
        value: float,
        field_name: str,
    ) -> float:
        try:
            normalized = float(value)
        except (TypeError, ValueError) as exc:
            raise IbkrPortfolioMappingError(
                f"{field_name} must be numeric."
            ) from exc

        if not math.isfinite(normalized):
            raise IbkrPortfolioMappingError(
                f"{field_name} must be finite."
            )

        if normalized <= 0:
            raise IbkrPortfolioMappingError(
                f"{field_name} must be greater than zero."
            )

        return normalized

    def _require_finite_non_negative(
        self,
        *,
        value: float,
        field_name: str,
    ) -> float:
        try:
            normalized = float(value)
        except (TypeError, ValueError) as exc:
            raise IbkrPortfolioMappingError(
                f"{field_name} must be numeric."
            ) from exc

        if not math.isfinite(normalized):
            raise IbkrPortfolioMappingError(
                f"{field_name} must be finite."
            )

        if normalized < 0:
            raise IbkrPortfolioMappingError(
                f"{field_name} must not be negative."
            )

        return normalized
