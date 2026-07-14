from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class QuoteValidationResult:
    """
    Result of deterministic quote validation.

    A valid trading price must:

    - be convertible to float;
    - be finite;
    - be greater than zero.
    """

    valid: bool
    symbol: str
    original_value: object
    normalized_price: float | None
    reason: str
    evaluated_at: datetime


class QuoteValidationService:
    """
    Central validation layer for prices received from providers,
    brokers and internal execution services.

    This service contains no provider-specific logic and may later
    be reused for Yahoo, IBKR and other market-data sources.
    """

    def validate(
        self,
        *,
        symbol: str,
        value: object,
    ) -> QuoteValidationResult:
        normalized_symbol = self._normalize_symbol(
            symbol
        )

        evaluated_at = datetime.now(UTC)

        if value is None:
            return QuoteValidationResult(
                valid=False,
                symbol=normalized_symbol,
                original_value=value,
                normalized_price=None,
                reason="Quote value is missing.",
                evaluated_at=evaluated_at,
            )

        if isinstance(value, bool):
            return QuoteValidationResult(
                valid=False,
                symbol=normalized_symbol,
                original_value=value,
                normalized_price=None,
                reason="Boolean values are not valid prices.",
                evaluated_at=evaluated_at,
            )

        try:
            normalized_price = float(value)

        except (TypeError, ValueError, OverflowError):
            return QuoteValidationResult(
                valid=False,
                symbol=normalized_symbol,
                original_value=value,
                normalized_price=None,
                reason="Quote value cannot be converted to float.",
                evaluated_at=evaluated_at,
            )

        if not math.isfinite(normalized_price):
            return QuoteValidationResult(
                valid=False,
                symbol=normalized_symbol,
                original_value=value,
                normalized_price=None,
                reason="Quote value is not finite.",
                evaluated_at=evaluated_at,
            )

        if normalized_price <= 0:
            return QuoteValidationResult(
                valid=False,
                symbol=normalized_symbol,
                original_value=value,
                normalized_price=None,
                reason="Quote price must be greater than zero.",
                evaluated_at=evaluated_at,
            )

        return QuoteValidationResult(
            valid=True,
            symbol=normalized_symbol,
            original_value=value,
            normalized_price=normalized_price,
            reason="Quote price is valid.",
            evaluated_at=evaluated_at,
        )

    def require_valid_price(
        self,
        *,
        symbol: str,
        value: object,
    ) -> float:
        """
        Returns a validated float price.

        Raises ValueError when the supplied quote is invalid.
        """

        result = self.validate(
            symbol=symbol,
            value=value,
        )

        if not result.valid:
            raise ValueError(
                "Invalid quote for "
                f"{result.symbol}: "
                f"{result.original_value!r}. "
                f"{result.reason}"
            )

        if result.normalized_price is None:
            raise RuntimeError(
                "Validated quote unexpectedly has no price."
            )

        return result.normalized_price

    def is_valid_price(
        self,
        *,
        symbol: str,
        value: object,
    ) -> bool:
        return self.validate(
            symbol=symbol,
            value=value,
        ).valid

    def _normalize_symbol(
        self,
        symbol: str,
    ) -> str:
        normalized_symbol = str(
            symbol
        ).strip().upper()

        if not normalized_symbol:
            raise ValueError(
                "Symbol is required for quote validation."
            )

        return normalized_symbol