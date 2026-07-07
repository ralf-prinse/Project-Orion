from __future__ import annotations

from dataclasses import dataclass

from models.strategy_hypothesis import StrategyHypothesis


@dataclass(frozen=True)
class HypothesisEvaluation:
    """
    Immutable evaluation result for a single strategy hypothesis.

    This object describes whether the available trading data supports,
    rejects or is insufficient to evaluate a hypothesis.

    It never modifies strategy settings.
    It contains no business logic.
    """

    hypothesis: StrategyHypothesis

    sample_size: int

    metric_value: float

    expected_value: float

    confidence: float

    supported: bool

    status: str
    reason: str

    @property
    def sufficient_data(self) -> bool:
        return self.sample_size >= self.hypothesis.minimum_sample_size