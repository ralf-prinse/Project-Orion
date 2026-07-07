from __future__ import annotations

from dataclasses import dataclass

from models.strategy_hypothesis import StrategyHypothesis


@dataclass(frozen=True)
class HypothesisEvaluationContext:
    """
    Immutable input context for HypothesisEvaluator.

    This keeps Sprint 7E aligned with Orion's standard architecture:

    Context
        ↓
    Engine
        ↓
    Result
    """

    hypothesis: StrategyHypothesis
    sample_size: int
    metric_value: float
    expected_value: float