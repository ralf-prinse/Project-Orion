from __future__ import annotations

from dataclasses import dataclass

from models.live_paper_trading_result import LivePaperCandidate
from services.risk.models import RiskResult


@dataclass(frozen=True)
class PortfolioAllocationDecision:
    """
    One deterministic portfolio allocation decision.

    This model only describes whether a candidate should be executed.
    It does not execute trades.
    """

    candidate: LivePaperCandidate
    quantity: int
    approved: bool
    reason: str
    risk_result: RiskResult | None = None
    fx_rate_to_base: float = 1.0

    @property
    def symbol(self) -> str:
        return self.candidate.symbol

    @property
    def estimated_value(self) -> float:
        return round(
            self.quantity
            * self.candidate.result.risk_plan.entry_price
            * self.fx_rate_to_base,
            2,
        )


@dataclass(frozen=True)
class PortfolioAllocationResult:
    """
    Immutable result of portfolio allocation.

    Contains all allocation decisions, both approved and rejected.
    """

    decisions: list[PortfolioAllocationDecision]

    @property
    def approved(self) -> list[PortfolioAllocationDecision]:
        return [
            decision
            for decision in self.decisions
            if decision.approved
        ]

    @property
    def rejected(self) -> list[PortfolioAllocationDecision]:
        return [
            decision
            for decision in self.decisions
            if not decision.approved
        ]

    @property
    def approved_count(self) -> int:
        return len(self.approved)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)

    @property
    def risk_evaluated(self) -> list[PortfolioAllocationDecision]:
        return [
            decision
            for decision in self.decisions
            if decision.risk_result is not None
        ]

    @property
    def risk_rejected(self) -> list[PortfolioAllocationDecision]:
        return [
            decision
            for decision in self.risk_evaluated
            if not decision.risk_result.risk_allowed
        ]
