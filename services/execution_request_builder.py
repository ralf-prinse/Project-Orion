from __future__ import annotations

from models.execution_request import ExecutionRequest
from models.risk_plan import RiskPlan


class ExecutionRequestBuilder:
    """
    Builds ExecutionRequest objects from deterministic pipeline output.

    No execution.
    No broker logic.
    No AI.
    """

    def build(
        self,
        pipeline_output: dict,
        quantity: int,
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
        )