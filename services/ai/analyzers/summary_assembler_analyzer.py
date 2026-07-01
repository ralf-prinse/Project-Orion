from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class SummaryAssemblerAnalyzer(BaseAIExplanationAnalyzer):
    """
    Assembleert de uiteindelijke deterministische samenvatting.
    """

    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        if not explanation_result.valid_explanation:
            explanation_result.summary = (
                "Orion kan nog geen uitleg genereren omdat er geen "
                "deterministische bronresultaten zijn meegegeven."
            )
            return explanation_result

        section_count = len(explanation_result.sections)
        symbol = explanation_result.symbol or explanation_context.resolved_symbol()
        title = explanation_context.title or f"Orion-uitleg voor {symbol}"
        explanation_result.title = title

        explanation_result.summary = (
            f"{title}: deze uitleg is deterministisch opgebouwd uit "
            f"{explanation_result.source_count} bronresulta(a)t(en) en "
            f"{section_count} uitlegsectie(s). AI neemt geen investeringsbeslissing; "
            "AI vat uitsluitend Orion-resultaten samen."
        )
        return explanation_result
