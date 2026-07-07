from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class TradingPipelineResult:
    """
    Immutable result returned by TradingPipeline.

    This object is the single contract between the TradingPipeline and
    downstream orchestration layers.

    Sprint 6E keeps temporary dictionary compatibility so older scanners,
    backtests and tests keep working during migration.
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
    pipeline_output: dict[str, Any] = field(default_factory=dict)

    @property
    def legacy_output(self) -> dict[str, Any]:
        return self.pipeline_output

    def to_dict(self) -> dict[str, Any]:
        return {
            "pipeline": self.pipeline_output,
            "ai_context": self.ai_context,
            "explanation": self.explanation,
        }

    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_dict().get(key, default)

    def items(self):
        return self.to_dict().items()

    def keys(self):
        return self.to_dict().keys()

    def values(self):
        return self.to_dict().values()

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict())

    def __contains__(self, key: str) -> bool:
        return key in self.to_dict()