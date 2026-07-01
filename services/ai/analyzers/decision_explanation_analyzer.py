from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class DecisionExplanationAnalyzer(BaseAIExplanationAnalyzer):
    """
    Zet DecisionResult deterministisch om naar een uitlegsectie.
    """

    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        decision = explanation_context.decision_result
        if decision is None:
            return explanation_result

        action = getattr(getattr(decision, "action", ""), "value", getattr(decision, "action", ""))
        bullets = [
            f"Beslissing: {action}.",
            f"Confidence: {getattr(decision, 'confidence', 0)}.",
            f"Risk level: {getattr(decision, 'risk_level', 0)}.",
        ]

        position_sizing = getattr(decision, "position_sizing", None)
        if position_sizing is not None:
            bullets.append(
                "Position sizing: "
                f"{getattr(position_sizing, 'recommended_shares', 0)} aandelen, "
                f"positieomvang {getattr(position_sizing, 'position_value', 0.0)}."
            )

        if explanation_config.include_reasons:
            bullets.extend(self._limited_items(getattr(decision, "reasons", []), explanation_config))
        if explanation_config.include_warnings:
            bullets.extend(self._warning_items(getattr(decision, "warnings", []), explanation_config))

        explanation_result.add_section("Decision explanation", bullets)
        return explanation_result

    def _limited_items(
        self,
        items: list[str],
        explanation_config: AIExplanationConfig,
    ) -> list[str]:
        return [f"Reden: {item}" for item in items[: explanation_config.max_bullets_per_section]]

    def _warning_items(
        self,
        items: list[str],
        explanation_config: AIExplanationConfig,
    ) -> list[str]:
        return [
            f"Waarschuwing: {item}"
            for item in items[: explanation_config.max_bullets_per_section]
        ]
