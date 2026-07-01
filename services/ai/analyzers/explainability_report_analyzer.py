from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class ExplainabilityReportAnalyzer(BaseAIExplanationAnalyzer):
    """
    Verwerkt het bestaande Explainability Framework tot uitlegbullets.
    """

    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        report = explanation_context.explanation_report
        if report is None:
            return explanation_result

        bullets = []
        for item in report.items[: explanation_config.max_bullets_per_section]:
            severity = getattr(item.severity, "value", str(item.severity))
            bullets.append(f"{severity}: {item.title} — {item.message}")

        if report.has_blockers():
            explanation_result.add_warning(
                "Explainability report bevat één of meer blockers."
            )

        explanation_result.add_section("Structured explainability", bullets)
        return explanation_result
