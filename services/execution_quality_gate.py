from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class ExecutionQuote:
    symbol: str
    bid: float
    ask: float
    received_at: datetime
    bid_size: float = 0.0
    ask_size: float = 0.0


@dataclass(frozen=True)
class ExecutionQualityDecision:
    allowed: bool
    reason: str
    spread_pct: float | None = None
    marketable_limit_price: float | None = None


class ExecutionQualityGate:
    """Fail-closed validation of an executable top-of-book quote."""

    def evaluate(
        self,
        *,
        quote: ExecutionQuote,
        side: str,
        max_spread_pct: float,
        max_quote_age_seconds: float,
        max_slippage_pct: float,
        required_quantity: int = 0,
        planned_price: float | None = None,
        now: datetime | None = None,
    ) -> ExecutionQualityDecision:
        normalized_side = side.strip().upper()
        if normalized_side not in {"BUY", "SELL"}:
            return ExecutionQualityDecision(False, "Unsupported order side.")

        values = (quote.bid, quote.ask)
        if any(not math.isfinite(value) or value <= 0 for value in values):
            return ExecutionQualityDecision(
                False,
                "IBKR bid/ask is missing or invalid.",
            )
        if quote.ask < quote.bid:
            return ExecutionQualityDecision(
                False,
                "IBKR ask is below bid; quote is inconsistent.",
            )

        if planned_price is not None:
            if not math.isfinite(planned_price) or planned_price <= 0:
                return ExecutionQualityDecision(
                    False,
                    "Planned execution price is invalid.",
                )
            worst_reference = (
                quote.ask if normalized_side == "BUY" else quote.bid
            )
            adverse_move = (
                (worst_reference - planned_price) / planned_price
                if normalized_side == "BUY"
                else (planned_price - worst_reference) / planned_price
            )
            if adverse_move > max_slippage_pct:
                return ExecutionQualityDecision(
                    False,
                    "Current executable price moved beyond the planned "
                    "slippage limit.",
                )

        if required_quantity > 0 and (
            quote.bid_size < required_quantity
            or quote.ask_size < required_quantity
        ):
            return ExecutionQualityDecision(
                False,
                "Top-of-book size cannot absorb the proposed order.",
            )

        evaluated_at = now or datetime.now(UTC)
        received_at = quote.received_at
        if received_at.tzinfo is None:
            received_at = received_at.replace(tzinfo=UTC)
        age_seconds = (evaluated_at - received_at).total_seconds()
        if age_seconds < 0 or age_seconds > max_quote_age_seconds:
            return ExecutionQualityDecision(
                False,
                f"IBKR quote is stale ({age_seconds:.2f} seconds).",
            )

        midpoint = (quote.bid + quote.ask) / 2.0
        spread_pct = (quote.ask - quote.bid) / midpoint
        if spread_pct > max_spread_pct:
            return ExecutionQualityDecision(
                False,
                "Bid/ask spread exceeds configured execution limit.",
                spread_pct=round(spread_pct, 6),
            )

        reference = quote.ask if normalized_side == "BUY" else quote.bid
        multiplier = (
            1.0 + max_slippage_pct
            if normalized_side == "BUY"
            else 1.0 - max_slippage_pct
        )
        limit_price = round(reference * multiplier, 4)
        return ExecutionQualityDecision(
            True,
            "Executable IBKR quote passed spread and freshness checks.",
            spread_pct=round(spread_pct, 6),
            marketable_limit_price=limit_price,
        )
