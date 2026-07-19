from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from models.execution_context import ExecutionContext
from models.position_state import PositionState
from models.trading_pipeline_result import TradingPipelineResult
from models.trading_session import TradingSession
from services.execution_engine import (
    ExecutionEngine,
    ExecutionEngineResult,
)
from services.execution_request_builder import ExecutionRequestBuilder


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

    TradingSession is the sole runtime owner of:
    - portfolio
    - PositionState
    - RiskPlan
    """

    def __init__(
        self,
        execution_engine: ExecutionEngine | None = None,
        request_builder: ExecutionRequestBuilder | None = None,
    ):
        self.execution_engine = execution_engine or ExecutionEngine()
        self.request_builder = request_builder or ExecutionRequestBuilder()

    def open_position(
        self,
        session: TradingSession,
        pipeline_output: TradingPipelineResult | dict[str, Any],
        quantity: int,
        fx_rate_to_base: float = 1.0,
        currency: str = "EUR",
    ) -> PaperTradeResult:
        request = self.request_builder.build(
            pipeline_output=pipeline_output,
            quantity=quantity,
            fx_rate_to_base=fx_rate_to_base,
            currency=currency,
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
            peak_portfolio_value=session.peak_portfolio_value,
        )

        position_state: PositionState | None = None

        if execution.execution.accepted:
            symbol = request.symbol.upper()

            position_state = PositionState(
                symbol=symbol,
                trade_id=str(uuid4()),
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

        return PaperTradeResult(
            executed=execution.execution.accepted,
            symbol=request.symbol.upper(),
            session=updated_session,
            execution=execution,
            position_state=position_state,
            message=execution.execution.message,
        )
