from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class TradingPipelineResult:
    """
    Immutable result returned by TradingPipeline.

    This object is the single contract between the TradingPipeline and
    downstream orchestration layers.

    It intentionally replaces anonymous dictionaries while remaining
    temporarily backwards compatible through the `pipeline_output`
    property.
    """

    symbol: str

    decision: str

    confidence: float

    position_size: int

    expected_risk: float

    risk_plan: RiskPlan

    market_intelligence: Any

    ai_context: str

    explanation: str

    pipeline_output: dict[str, Any] = field(default_factory=dict)

    @property
    def legacy_output(self) -> dict[str, Any]:
        """
        Temporary backwards-compatible interface.

        Existing services can continue reading dictionary keys while the
        architecture migrates to strongly typed models.
        """
        return self.pipeline_output

    def to_dict(self) -> dict[str, Any]:
        """
        Temporary compatibility helper.

        New code should consume TradingPipelineResult directly.
        """
        return {
            "symbol": self.symbol,
            "decision": self.decision,
            "confidence": self.confidence,
            "position_size": self.position_size,
            "expected_risk": self.expected_risk,
            "risk_plan": self.risk_plan,
            "market_intelligence": self.market_intelligence,
            "ai_context": self.ai_context,
            "explanation": self.explanation,
            "pipeline_output": self.pipeline_output,
        }