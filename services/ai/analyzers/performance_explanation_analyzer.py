from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class PerformanceExplanationAnalyzer(BaseAIExplanationAnalyzer):
    """
    Zet PerformanceResult deterministisch om naar een professionele uitlegsectie.
    """

    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        performance = explanation_context.performance_result
        if performance is None:
            return explanation_result

        bullets = [
            f"Aantal trades: {getattr(performance, 'total_trades', 0)}.",
            f"Winrate: {getattr(performance, 'win_rate', 0.0)}%.",
            f"Netto P/L: {getattr(performance, 'net_pnl', 0.0)}.",
            f"Profit factor: {getattr(performance, 'profit_factor', 0.0)}.",
            f"Max drawdown: {getattr(performance, 'max_drawdown_pct', 0.0)}%.",
            f"Expectancy: {getattr(performance, 'expectancy', 0.0)}.",
        ]

        if explanation_config.include_warnings:
            bullets.extend(
                f"Waarschuwing: {warning}"
                for warning in getattr(performance, "warnings", [])[
                    : explanation_config.max_bullets_per_section
                ]
            )

        explanation_result.add_section("Performance explanation", bullets)
        return explanation_result
