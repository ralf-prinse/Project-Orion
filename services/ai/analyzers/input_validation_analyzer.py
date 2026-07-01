from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class InputValidationAnalyzer(BaseAIExplanationAnalyzer):
    """
    Valideert of er deterministische Orion-output beschikbaar is om uit te leggen.
    """

    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        sources = [
            explanation_context.decision_result,
            explanation_context.trade_plan_result,
            explanation_context.performance_result,
            explanation_context.explanation_report,
        ]
        explanation_result.source_count = sum(source is not None for source in sources)

        if explanation_result.source_count == 0:
            explanation_result.valid_explanation = False
            explanation_result.add_warning(
                "Geen deterministische Orion-resultaten beschikbaar om uit te leggen."
            )
            return explanation_result

        explanation_result.valid_explanation = True
        explanation_result.add_reason(
            "Uitleg is opgebouwd uit bestaande deterministische Orion-resultaten."
        )
        return explanation_result
