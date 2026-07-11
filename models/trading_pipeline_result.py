from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class TradingPipelineResult:
    """
    Immutable result returned by TradingPipeline.

    This object is the single typed contract between the TradingPipeline
    and downstream orchestration layers.

    No dictionary compatibility.
    No legacy accessors.
    No anonymous pipeline_output contract.
    """

    symbol: str
    decision: str
    confidence: float
    position_size: float
    expected_risk: float
    risk_plan: RiskPlan
    market_intelligence: Any
    ai_context: Any
    explanation: Any
    investment_thesis: Any | None = None
