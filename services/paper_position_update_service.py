from __future__ import annotations

from dataclasses import dataclass

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.position_state import PositionState
from models.trading_session import TradingSession
from services.position_update_engine import (
    PositionUpdateEngine,
    PositionUpdateResult,
)
from services.quote_validation_service import (
    QuoteValidationService,
)


@dataclass(frozen=True)
class PaperPositionUpdateResult:
    updated: bool
    symbol: str
    session: TradingSession
    position_update: PositionUpdateResult | None
    position_state: PositionState | None
    message: str


class PaperPositionUpdateService:
    """
    Updates one managed paper position.

    Invalid quotes are rejected without mutating TradingSession.
    The previously valid position price and lifecycle state remain
    unchanged.
    """

    def __init__(
        self,
        position_update_engine: (
            PositionUpdateEngine | None
        ) = None,
        quote_validation_service: (
            QuoteValidationService | None
        ) = None,
    ):
        self.position_update_engine = (
            position_update_engine
            or PositionUpdateEngine()
        )
        self.quote_validation_service = (
            quote_validation_service
            or QuoteValidationService()
        )

    def update_position(
        self,
        session: TradingSession,
        symbol: str,
        current_price: object,
    ) -> PaperPositionUpdateResult:
        normalized_symbol = str(
            symbol
        ).strip().upper()

        if not normalized_symbol:
            raise ValueError(
                "Position symbol is required."
            )

        position = (
            session.portfolio.positions.get(
                normalized_symbol
            )
        )
        state = session.position_states.get(
            normalized_symbol
        )
        risk_plan = session.risk_plans.get(
            normalized_symbol
        )

        if position is None:
            return self._not_updated(
                symbol=normalized_symbol,
                session=session,
                message="Position not found.",
            )

        if state is None:
            return self._not_updated(
                symbol=normalized_symbol,
                session=session,
                message="PositionState not found.",
            )

        if risk_plan is None:
            return self._not_updated(
                symbol=normalized_symbol,
                session=session,
                message="RiskPlan not found.",
            )

        quote = self.quote_validation_service.validate(
            symbol=normalized_symbol,
            value=current_price,
        )

        if (
            not quote.valid
            or quote.normalized_price is None
        ):
            return self._not_updated(
                symbol=normalized_symbol,
                session=session,
                message=(
                    "Invalid quote ignored. "
                    f"{quote.reason}"
                ),
            )

        validated_price = (
            quote.normalized_price
        )

        position_update = (
            self.position_update_engine.update(
                state=state,
                risk_plan=risk_plan,
                current_price=validated_price,
            )
        )

        updated_positions = dict(
            session.portfolio.positions
        )
        updated_positions[normalized_symbol] = (
            PaperPosition(
                symbol=normalized_symbol,
                quantity=position.quantity,
                entry_price=position.entry_price,
                current_price=validated_price,
                currency=position.currency,
                fx_rate_to_base=position.fx_rate_to_base,
            )
        )

        updated_states = dict(
            session.position_states
        )
        updated_states[normalized_symbol] = (
            position_update.state
        )

        updated_session = TradingSession(
            name=session.name,
            portfolio=PaperPortfolio(
                cash=session.portfolio.cash,
                positions=updated_positions,
                base_currency=session.portfolio.base_currency,
            ),
            position_states=updated_states,
            risk_plans=dict(
                session.risk_plans
            ),
            status=session.status,
            peak_portfolio_value=session.peak_portfolio_value,
        )

        return PaperPositionUpdateResult(
            updated=True,
            symbol=normalized_symbol,
            session=updated_session,
            position_update=position_update,
            position_state=position_update.state,
            message="Paper position updated.",
        )

    def _not_updated(
        self,
        *,
        symbol: str,
        session: TradingSession,
        message: str,
    ) -> PaperPositionUpdateResult:
        return PaperPositionUpdateResult(
            updated=False,
            symbol=symbol,
            session=session,
            position_update=None,
            position_state=None,
            message=message,
        )
