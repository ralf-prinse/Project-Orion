from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class TradePlanExplanationAnalyzer(BaseAIExplanationAnalyzer):
    """
    Zet TradePlanResult deterministisch om naar een uitvoerbare uitlegsectie.
    """

    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        trade_plan = explanation_context.trade_plan_result
        if trade_plan is None:
            return explanation_result

        bullets = [
            f"Plan geldig: {getattr(trade_plan, 'valid_plan', False)}.",
            f"Entry: {getattr(trade_plan, 'entry_price', 0.0)}.",
            f"Stop-loss: {getattr(trade_plan, 'stop_loss', 0.0)}.",
            f"Target: {getattr(trade_plan, 'target_price', 0.0)}.",
            f"Reward/risk: {getattr(trade_plan, 'reward_risk_ratio', 0.0)}.",
        ]

        shares = getattr(trade_plan, "shares", 0)
        if shares:
            bullets.append(
                f"Aantal aandelen: {shares}; positieomvang: "
                f"{getattr(trade_plan, 'position_value', 0.0)}."
            )

        if explanation_config.include_warnings:
            bullets.extend(
                f"Waarschuwing: {warning}"
                for warning in getattr(trade_plan, "warnings", [])[
                    : explanation_config.max_bullets_per_section
                ]
            )

        explanation_result.add_section("Trade plan explanation", bullets)
        return explanation_result
