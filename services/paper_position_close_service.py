from __future__ import annotations

from dataclasses import dataclass

from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession


@dataclass(frozen=True)
class PaperPositionCloseResult:
    closed: bool
    symbol: str
    session: TradingSession
    exit_price: float
    realized_profit_loss: float
    message: str


class PaperPositionCloseService:
    def close_position(
        self,
        session: TradingSession,
        symbol: str,
        exit_price: float,
    ) -> PaperPositionCloseResult:
        normalized_symbol = str(symbol).strip().upper()
        position = session.portfolio.positions.get(normalized_symbol)

        if position is None:
            return PaperPositionCloseResult(
                False,
                normalized_symbol,
                session,
                float(exit_price),
                0.0,
                "Position not found.",
            )

        position_value = round(
            position.quantity * float(exit_price),
            2,
        )
        cost_basis = round(
            position.quantity * position.entry_price,
            2,
        )
        realized_profit_loss = round(
            position_value - cost_basis,
            2,
        )

        updated_positions = dict(session.portfolio.positions)
        updated_positions.pop(normalized_symbol, None)

        updated_states = dict(session.position_states)
        updated_states.pop(normalized_symbol, None)

        updated_risk_plans = dict(session.risk_plans)
        updated_risk_plans.pop(normalized_symbol, None)

        updated_session = TradingSession(
            name=session.name,
            portfolio=PaperPortfolio(
                cash=round(session.portfolio.cash + position_value, 2),
                positions=updated_positions,
            ),
            position_states=updated_states,
            risk_plans=updated_risk_plans,
            status=session.status,
        )

        return PaperPositionCloseResult(
            True,
            normalized_symbol,
            updated_session,
            round(float(exit_price), 2),
            realized_profit_loss,
            "Paper position closed.",
        )
