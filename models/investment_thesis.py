from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ThesisStance = Literal["BUY", "WATCH", "AVOID"]


@dataclass(frozen=True)
class ThesisFactor:
    """One transparent deterministic contribution to an investment thesis."""

    name: str
    score: float
    weight: float
    contribution: float
    rationale: str


@dataclass(frozen=True)
class InvestmentThesis:
    """
    Explainable strategy assessment produced beside the active decision.

    The thesis is initially used in shadow mode. It does not approve trades,
    size positions, mutate TradingSession, or execute exits.
    """

    symbol: str
    stance: ThesisStance
    conviction: float
    quality: float
    factors: tuple[ThesisFactor, ...]
    supporting_reasons: tuple[str, ...]
    risk_reasons: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    summary: str
