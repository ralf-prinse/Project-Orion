from __future__ import annotations

from dataclasses import dataclass

from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class BreakEvenResult:
    """
    Result of deterministic break-even evaluation.

    No trade execution.
    No AI.
    No persistence.
    """

    activated: bool
    new_stop_loss: float
    reason: str


class BreakEvenService:
    """
    Determines whether a trade should move its stop-loss
    to break-even.

    Rules
    -----
    - Never lowers the stop-loss.
    - Never changes targets.
    - Never exits a trade.
    - Only protects capital.
    """

    def evaluate(
        self,
        risk_plan: RiskPlan,
        current_price: float,
    ) -> BreakEvenResult:

        entry = float(risk_plan.entry_price)
        stop = float(risk_plan.stop_loss)
        target_1 = float(risk_plan.target_1)

        if current_price < target_1:
            return BreakEvenResult(
                activated=False,
                new_stop_loss=stop,
                reason="Target 1 not reached.",
            )

        new_stop = max(stop, entry)

        if new_stop == stop:
            return BreakEvenResult(
                activated=False,
                new_stop_loss=stop,
                reason="Break-even already active.",
            )

        return BreakEvenResult(
            activated=True,
            new_stop_loss=round(new_stop, 2),
            reason="Target 1 reached. Stop moved to break-even.",
        )