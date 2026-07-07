from __future__ import annotations

from dataclasses import dataclass

from models.execution_context import ExecutionContext
from models.paper_portfolio import PaperPortfolio
from models.position_state import PositionState
from models.trading_session import TradingSession
from services.execution_engine import (
    ExecutionEngine,
    ExecutionEngineResult,
)
from services.execution_request_builder import ExecutionRequestBuilder
from services.position_state_store import PositionStateStore


@dataclass(frozen=True)
class PaperTradeResult:
    """
    Result of one end-to-end paper trade.

    No live broker.
    No real money.
    No AI.
    """

    executed: bool
    symbol: str
    session: TradingSession
    execution: ExecutionEngineResult
    position_state: PositionState | None
    message: str


class PaperTradingService:
    """
    Executes one deterministic paper trade from pipeline output.

    Responsibilities
    ----------------
    - Build ExecutionRequest
    - Build ExecutionContext
    - Run ExecutionEngine
    - Update TradingSession portfolio
    - Create PositionState for filled paper positions
    - Save PositionState in PositionStateStore

    Does NOT
    --------
    - Scan markets
    - Generate BUY/HOLD/SELL
    - Generate RiskPlan
    - Execute real broker orders
    """

    def __init__(
        self,
        execution_engine: ExecutionEngine | None = None,
        request_builder: ExecutionRequestBuilder | None = None,
        position_state_store: PositionStateStore | None = None,
    ):
        self.execution_engine = execution_engine or ExecutionEngine()
        self.request_builder = request_builder or ExecutionRequestBuilder()
        self.position_state_store = (
            position_state_store
            or PositionStateStore()
        )

    def open_position(
        self,
        session: TradingSession,
        pipeline_output: dict,
        quantity: int,
    ) -> PaperTradeResult:

        request = self.request_builder.build(
            pipeline_output=pipeline_output,
            quantity=quantity,
        )

        context = ExecutionContext(
            request=request,
            portfolio=session.portfolio,
            trading_mode="PAPER",
            max_position_percentage=1.0,
            allow_fractional_shares=False,
        )

        execution = self.execution_engine.execute(context)

        updated_session = TradingSession(
            name=session.name,
            portfolio=execution.portfolio,
            position_states=dict(session.position_states),
            status=session.status,
        )

        position_state: PositionState | None = None

        if execution.execution.accepted:
            position_state = PositionState(
                symbol=request.symbol,
                entry_price=request.risk_plan.entry_price,
                current_stop_loss=request.risk_plan.stop_loss,
                highest_price=request.risk_plan.entry_price,
                current_price=request.risk_plan.entry_price,
                break_even_active=False,
                trailing_stop_active=False,
                target_1_hit=False,
                target_2_hit=False,
                target_3_hit=False,
            )

            updated_session.position_states[
                request.symbol
            ] = position_state

            self.position_state_store.save(position_state)

        return PaperTradeResult(
            executed=execution.execution.accepted,
            symbol=request.symbol,
            session=updated_session,
            execution=execution,
            position_state=position_state,
            message=execution.execution.message,
        )