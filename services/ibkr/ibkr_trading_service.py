from __future__ import annotations

from collections.abc import Mapping

from models.trading_pipeline_result import TradingPipelineResult
from services.execution_request_builder import (
    ExecutionRequestBuilder,
)
from services.ibkr.ibkr_execution_service import (
    IbkrExecutionService,
)


class IbkrTradingService:
    """
    Orchestrates one complete controlled IBKR Paper trade.

    This service only connects existing Orion components. It does not
    generate decisions, calculate quantity or own lifecycle state.
    """

    def __init__(
        self,
        *,
        request_builder: ExecutionRequestBuilder,
        execution_service: IbkrExecutionService,
    ) -> None:
        self._request_builder = request_builder
        self._execution_service = execution_service

    def execute_trade(
        self,
        *,
        pipeline_result: TradingPipelineResult,
        quantity: int,
        current_prices: Mapping[str, float],
    ):
        if not isinstance(quantity, int):
            raise ValueError(
                "IBKR trade quantity must be an integer."
            )

        if quantity <= 0:
            raise ValueError(
                "IBKR trade quantity must be greater than zero."
            )

        request = self._request_builder.build(
            pipeline_output=pipeline_result,
            quantity=quantity,
        )

        return self._execution_service.execute(
            request=request,
            current_prices=current_prices,
        )