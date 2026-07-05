from __future__ import annotations

from dataclasses import dataclass

from services.orchestration.live_scanner_service import LiveScannerSnapshot
from services.position_sizing_service import (
    PositionSizingResult,
    PositionSizingService,
)


@dataclass(frozen=True)
class Opportunity:
    symbol: str
    price: float
    signal: str
    technical_score: float
    reason: str
    analysis: object | None
    position_sizing: PositionSizingResult | None = None


class OpportunityService:
    """
    Builds deterministic Mission Control opportunities.

    Combines scanner results, quote prices and position sizing into one
    presentation-ready domain model.

    This service does not create BUY / HOLD / SELL decisions.
    TradingPipeline and scanner output remain the source of signals.
    """

    def __init__(
        self,
        position_sizing_service: PositionSizingService | None = None,
    ) -> None:
        self._position_sizing_service = (
            position_sizing_service or PositionSizingService()
        )

    def build_opportunities(
        self,
        snapshot: LiveScannerSnapshot,
        available_cash: float,
        limit: int = 5,
    ) -> tuple[Opportunity, ...]:
        quote_map = {
            quote.symbol: quote
            for quote in snapshot.quotes
        }

        opportunities: list[Opportunity] = []

        for result in snapshot.top_results[:limit]:
            symbol = str(getattr(result, "symbol", "")).strip().upper()

            if not symbol:
                continue

            quote = quote_map.get(symbol)

            if quote is None:
                continue

            price = float(getattr(quote, "price", 0.0))

            sizing = None

            if available_cash > 0 and price > 0:
                sizing = self._position_sizing_service.calculate(
                    symbol=symbol,
                    available_cash=available_cash,
                    price=price,
                )

            opportunities.append(
                Opportunity(
                    symbol=symbol,
                    price=price,
                    signal=getattr(result, "signal", ""),
                    technical_score=float(getattr(result, "technical_score", 0.0)),
                    reason=getattr(result, "reason", ""),
                    analysis=getattr(result, "analysis", None),
                    position_sizing=sizing,
                )
            )

        return tuple(opportunities)