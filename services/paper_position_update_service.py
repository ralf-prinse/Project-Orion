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


@dataclass(frozen=True)
class PaperPositionUpdateResult:
    updated: bool
    symbol: str
    session: TradingSession
    position_update: PositionUpdateResult | None
    position_state: PositionState | None
    message: str


class PaperPositionUpdateService:
    def __init__(
        self,
        position_update_engine: PositionUpdateEngine | None = None,
    ):
        self.position_update_engine = (
            position_update_engine or PositionUpdateEngine()
        )

    def update_position(
        self,
        session: TradingSession,
        symbol: str,
        current_price: float,
    ) -> PaperPositionUpdateResult:
        normalized_symbol = str(symbol).strip().upper()

        position = session.portfolio.positions.get(normalized_symbol)
        state = session.position_states.get(normalized_symbol)
        risk_plan = session.risk_plans.get(normalized_symbol)

        if position is None:
            return PaperPositionUpdateResult(
                False,
                normalized_symbol,
                session,
                None,
                None,
                "Position not found.",
            )

        if state is None:
            return PaperPositionUpdateResult(
                False,
                normalized_symbol,
                session,
                None,
                None,
                "PositionState not found.",
            )

        if risk_plan is None:
            return PaperPositionUpdateResult(
                False,
                normalized_symbol,
                session,
                None,
                None,
                "RiskPlan not found.",
            )

        position_update = self.position_update_engine.update(
            state=state,
            risk_plan=risk_plan,
            current_price=current_price,
        )

        updated_positions = dict(session.portfolio.positions)
        updated_positions[normalized_symbol] = PaperPosition(
            symbol=normalized_symbol,
            quantity=position.quantity,
            entry_price=position.entry_price,
            current_price=current_price,
        )

        updated_states = dict(session.position_states)
        updated_states[normalized_symbol] = position_update.state

        updated_session = TradingSession(
            name=session.name,
            portfolio=PaperPortfolio(
                cash=session.portfolio.cash,
                positions=updated_positions,
            ),
            position_states=updated_states,
            risk_plans=dict(session.risk_plans),
            status=session.status,
        )

        return PaperPositionUpdateResult(
            True,
            normalized_symbol,
            updated_session,
            position_update,
            position_update.state,
            "Paper position updated.",
        )
