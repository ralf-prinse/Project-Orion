from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.execution_context import ExecutionContext
from models.position_state import PositionState
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from services.execution_engine import (
    ExecutionEngine,
    ExecutionEngineResult,
)
from services.execution_request_builder import ExecutionRequestBuilder
from services.position_state_store import PositionStateStore


@dataclass(frozen=True)
class PaperTradeResult:
    executed: bool
    symbol: str
    session: TradingSession
    execution: ExecutionEngineResult
    position_state: PositionState | None
    message: str


class PaperTradingService:
    """
    Opens paper positions inside a TradingSession.

    Runtime ownership:
    - TradingSession owns the portfolio, PositionState and RiskPlan.
    - PositionStateStore remains a shared compatibility/runtime store
      until its separate consolidation step.
    - Persistence of a complete TradingSession is owned by the runner
      through TradingSessionRepository.

    This service does not own or persist a standalone PaperPortfolio.
    """

    def __init__(
        self,
        execution_engine: ExecutionEngine | None = None,
        request_builder: ExecutionRequestBuilder | None = None,
        position_state_store: PositionStateStore | None = None,
    ):
        self.execution_engine = (
            execution_engine
            or ExecutionEngine()
        )
        self.request_builder = (
            request_builder
            or ExecutionRequestBuilder()
        )
        self.position_state_store = (
            position_state_store
            or PositionStateStore()
        )

    def open_position(
        self,
        session: TradingSession,
        pipeline_output: TradingPipelineResult | dict[str, Any],
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
            risk_plans=dict(session.risk_plans),
            status=session.status,
        )

        position_state: PositionState | None = None

        if execution.execution.accepted:
            symbol = request.symbol.upper()

            position_state = PositionState(
                symbol=symbol,
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

            updated_session.position_states[symbol] = position_state
            updated_session.risk_plans[symbol] = request.risk_plan

            self.position_state_store.save(position_state)

        return PaperTradeResult(
            executed=execution.execution.accepted,
            symbol=request.symbol.upper(),
            session=updated_session,
            execution=execution,
            position_state=position_state,
            message=execution.execution.message,
        )
