from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class StrategyHypothesis:
    """
    Immutable description of one strategy hypothesis.

    A hypothesis is an idea Orion may evaluate, but never apply
    automatically.

    No AI.
    No execution.
    No configuration mutation.
    """

    hypothesis_id: str
    title: str
    description: str

    metric_name: str
    expected_direction: str
    minimum_sample_size: int

    created_at: datetime
    created_by: str = "ORION"

    tags: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""

    def __post_init__(self):
        if not self.hypothesis_id.strip():
            raise ValueError("hypothesis_id mag niet leeg zijn.")

        if not self.title.strip():
            raise ValueError("title mag niet leeg zijn.")

        if not self.metric_name.strip():
            raise ValueError("metric_name mag niet leeg zijn.")

        if self.expected_direction not in ("INCREASE", "DECREASE", "STABLE"):
            raise ValueError(
                "expected_direction moet INCREASE, DECREASE of STABLE zijn."
            )

        if self.minimum_sample_size < 1:
            raise ValueError("minimum_sample_size moet minimaal 1 zijn.")