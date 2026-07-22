from __future__ import annotations

from typing import Any
from uuid import uuid4

from models.execution_request import ExecutionRequest
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult


class ExecutionRequestBuilder:
    """
    Builds ExecutionRequest objects from deterministic pipeline output.

    Supports both:
    - TradingPipelineResult
    - legacy dictionary pipeline output

    No execution.
    No broker logic.
    No AI.
    """

    def build(
        self,
        pipeline_output: TradingPipelineResult | dict[str, Any],
        quantity: int,
        fx_rate_to_base: float = 1.0,
        currency: str = "EUR",
    ) -> ExecutionRequest:
        if isinstance(pipeline_output, TradingPipelineResult):
            return self._build_from_result(
                result=pipeline_output,
                quantity=quantity,
                fx_rate_to_base=fx_rate_to_base,
                currency=currency,
            )

        return self._build_from_legacy_dict(
            pipeline_output=pipeline_output,
            quantity=quantity,
            fx_rate_to_base=fx_rate_to_base,
            currency=currency,
        )

    def _build_from_result(
        self,
        result: TradingPipelineResult,
        quantity: int,
        fx_rate_to_base: float,
        currency: str,
    ) -> ExecutionRequest:
        return ExecutionRequest(
            symbol=result.symbol.upper(),
            action="OPEN_POSITION",
            entry_price=float(result.risk_plan.entry_price),
            quantity=int(quantity),
            risk_plan=result.risk_plan,
            confidence=float(result.confidence),
            strategy="DEFAULT",
            source="TradingPipeline",
            fx_rate_to_base=float(fx_rate_to_base),
            currency=currency.strip().upper(),
            trade_id=str(uuid4()),
        )

    def _build_from_legacy_dict(
        self,
        pipeline_output: dict[str, Any],
        quantity: int,
        fx_rate_to_base: float,
        currency: str,
    ) -> ExecutionRequest:
        risk_plan_data = pipeline_output["risk_plan"]

        risk_plan = RiskPlan(
            symbol=risk_plan_data["symbol"],
            entry_price=float(risk_plan_data["entry_price"]),
            stop_loss=float(risk_plan_data["stop_loss"]),
            target_1=float(risk_plan_data["target_1"]),
            target_2=float(risk_plan_data["target_2"]),
            target_3=float(risk_plan_data["target_3"]),
            risk_percent=float(risk_plan_data["risk_percent"]),
            reward_percent=float(risk_plan_data["reward_percent"]),
            risk_reward_ratio=float(risk_plan_data["risk_reward_ratio"]),
            confidence=float(risk_plan_data["confidence"]),
            notes=str(risk_plan_data.get("notes", "")),
        )

        return ExecutionRequest(
            symbol=str(pipeline_output["symbol"]).upper(),
            action="OPEN_POSITION",
            entry_price=float(risk_plan.entry_price),
            quantity=int(quantity),
            risk_plan=risk_plan,
            confidence=float(pipeline_output["confidence"]),
            strategy="DEFAULT",
            source="TradingPipeline",
            fx_rate_to_base=float(fx_rate_to_base),
            currency=currency.strip().upper(),
            trade_id=str(uuid4()),
        )
