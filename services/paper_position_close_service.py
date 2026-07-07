from __future__ import annotations

from dataclasses import dataclass

from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.position_state_store import PositionStateStore


@dataclass(frozen=True)
class PaperPositionCloseResult:
    """
    Result of closing one paper position.

    No live broker.
    No real money.
    No AI.
    """

    closed: bool
    symbol: str
    session: TradingSession
    exit_price: float
    realized_profit_loss: float
    message: str


class PaperPositionCloseService:
    """
    Closes an open paper position.

    Responsibilities
    ----------------
    - Add position value back to cash
    - Remove paper position
    - Remove PositionState
    - Remove RiskPlan reference
    - Remove PositionState from PositionStateStore

    Does NOT
    --------
    - Generate SELL decisions
    - Execute real broker orders
    - Use AI
    """

    def __init__(
        self,
        position_state_store: PositionStateStore | None = None,
    ):
        self.position_state_store = (
            position_state_store
            or PositionStateStore()
        )

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
                closed=False,
                symbol=normalized_symbol,
                session=session,
                exit_price=float(exit_price),
                realized_profit_loss=0.0,
                message="Position not found.",
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

        self.position_state_store.remove(normalized_symbol)

        return PaperPositionCloseResult(
            closed=True,
            symbol=normalized_symbol,
            session=updated_session,
            exit_price=round(float(exit_price), 2),
            realized_profit_loss=realized_profit_loss,
            message="Paper position closed.",
        )