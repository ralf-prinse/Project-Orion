from __future__ import annotations

from dataclasses import dataclass

from models.position_state import PositionState
from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class PositionHealthResult:
    """
    Deterministic health assessment for an open position.

    No BUY.
    No SELL.
    No EXIT.
    No AI.
    """

    status: str
    score: int
    warnings: list[str]
    summary: str


class PositionHealthService:
    """
    Evaluates the current health of an open position.

    This service does not decide whether to close a trade.
    It only explains the quality of the current position state.
    """

    def evaluate(
        self,
        state: PositionState,
        risk_plan: RiskPlan,
    ) -> PositionHealthResult:
        score = 100
        warnings: list[str] = []

        if state.current_price <= state.current_stop_loss:
            score -= 60
            warnings.append("Current price is at or below stop-loss.")

        if state.current_price < state.entry_price:
            score -= 20
            warnings.append("Position is trading below entry price.")

        if not state.target_1_hit:
            distance_to_target_1 = self._distance_percent(
                current=state.current_price,
                target=risk_plan.target_1,
            )

            if distance_to_target_1 > 8:
                score -= 10
                warnings.append("Position is still far from Target 1.")

        if state.break_even_active:
            score += 5

        if state.trailing_stop_active:
            score += 5

        if state.target_1_hit:
            score += 10

        if state.target_2_hit:
            score += 10

        if state.target_3_hit:
            score += 10

        score = max(0, min(100, score))
        status = self._status(score)

        return PositionHealthResult(
            status=status,
            score=score,
            warnings=warnings,
            summary=self._summary(status, score, warnings),
        )

    def _distance_percent(
        self,
        current: float,
        target: float,
    ) -> float:
        if current <= 0:
            return 100.0

        if target <= current:
            return 0.0

        return ((target - current) / current) * 100

    def _status(
        self,
        score: int,
    ) -> str:
        if score >= 85:
            return "EXCELLENT"

        if score >= 70:
            return "GOOD"

        if score >= 50:
            return "WEAK"

        return "CRITICAL"

    def _summary(
        self,
        status: str,
        score: int,
        warnings: list[str],
    ) -> str:
        if not warnings:
            return f"{status} position health with score {score}."

        return (
            f"{status} position health with score {score}. "
            + " ".join(warnings)
        )