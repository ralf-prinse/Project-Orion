from __future__ import annotations

from collections.abc import Mapping

from models.execution_request import ExecutionRequest
from services.execution_engine import ExecutionEngine
from services.ibkr.ibkr_execution_context_builder import (
    IbkrExecutionContextBuilder,
)


class IbkrExecutionService:
    """
    Executes one Orion execution request against an IBKR Paper account.

    Responsibilities:

    - build an ExecutionContext from the current IBKR Paper account
    - invoke the existing ExecutionEngine
    - return the existing ExecutionResult

    This service intentionally does not:

    - create ExecutionRequests
    - generate RiskPlans
    - make trading decisions
    - manage TradingSessions
    - own portfolio state
    """

    def __init__(
        self,
        *,
        context_builder: IbkrExecutionContextBuilder,
        execution_engine: ExecutionEngine,
    ) -> None:
        self._context_builder = context_builder
        self._execution_engine = execution_engine

    def execute(
        self,
        *,
        request: ExecutionRequest,
        current_prices: Mapping[str, float],
    ):
        """
        Execute one request using the existing Orion execution pipeline.
        """

        context = self._context_builder.build(
            request=request,
            current_prices=current_prices,
        )

        return self._execution_engine.execute(
            context
        )