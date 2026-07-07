from __future__ import annotations

from dataclasses import dataclass, field

from models.risk_plan import RiskPlan


@dataclass(frozen=True)
class RiskPlanValidationResult:
    """
    Deterministic validation result for a RiskPlan.

    No trading decisions.
    No AI.
    No persistence.
    """

    is_valid: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.errors:
            return "FAIL"

        if self.warnings:
            return "WARNING"

        return "PASS"


class RiskPlanValidator:
    """
    Validates deterministic RiskPlan consistency.

    Responsibilities
    ----------------
    - Check stop-loss validity
    - Check target ordering
    - Check risk/reward boundaries
    - Check risk percentage boundaries
    - Check whether risk model metadata is present

    Does NOT
    --------
    - Generate RiskPlans
    - Modify RiskPlans
    - Generate BUY/HOLD/SELL decisions
    - Execute trades
    """

    MIN_RISK_PERCENT = 1.0
    MAX_RISK_PERCENT = 10.0
    MIN_RISK_REWARD_RATIO = 1.4

    def validate(
        self,
        risk_plan: RiskPlan,
    ) -> RiskPlanValidationResult:

        warnings: list[str] = []
        errors: list[str] = []

        entry = float(risk_plan.entry_price)
        stop_loss = float(risk_plan.stop_loss)
        target_1 = float(risk_plan.target_1)
        target_2 = float(risk_plan.target_2)
        target_3 = float(risk_plan.target_3)

        if not risk_plan.symbol:
            errors.append("Symbol is missing.")

        if entry <= 0:
            errors.append("Entry price must be greater than zero.")

        if stop_loss <= 0:
            errors.append("Stop-loss must be greater than zero.")

        if entry > 0 and stop_loss >= entry:
            errors.append("Stop-loss must be below entry price.")

        if target_1 <= entry:
            errors.append("Target 1 must be above entry price.")

        if target_2 <= target_1:
            errors.append("Target 2 must be above Target 1.")

        if target_3 <= target_2:
            errors.append("Target 3 must be above Target 2.")

        if risk_plan.risk_percent <= 0:
            errors.append("Risk percentage must be greater than zero.")

        if risk_plan.risk_reward_ratio <= 0:
            errors.append("Risk/reward ratio must be greater than zero.")

        if (
            risk_plan.risk_percent > 0
            and risk_plan.risk_percent < self.MIN_RISK_PERCENT
        ):
            warnings.append(
                f"Risk percentage is very tight: {risk_plan.risk_percent:.2f}%."
            )

        if risk_plan.risk_percent > self.MAX_RISK_PERCENT:
            warnings.append(
                f"Risk percentage is high: {risk_plan.risk_percent:.2f}%."
            )

        if (
            risk_plan.risk_reward_ratio > 0
            and risk_plan.risk_reward_ratio < self.MIN_RISK_REWARD_RATIO
        ):
            warnings.append(
                "Risk/reward ratio is below preferred minimum: "
                f"{risk_plan.risk_reward_ratio:.2f}."
            )

        notes = str(risk_plan.notes)

        if "stop_model=" not in notes:
            warnings.append("RiskPlan does not include stop_model metadata.")

        if "atr=" not in notes:
            warnings.append("RiskPlan does not include ATR metadata.")

        return RiskPlanValidationResult(
            is_valid=not errors,
            warnings=warnings,
            errors=errors,
        )