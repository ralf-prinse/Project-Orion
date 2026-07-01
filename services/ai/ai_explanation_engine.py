from core.orchestration.analyzer_runner import AnalyzerRunner
from services.ai.ai_explanation_registry import AIExplanationRegistry
from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class AIExplanationEngine:
    """
    Centrale AI Explanation Engine van Project Orion.

    Deze foundation maakt deterministische uitleg op basis van bestaande
    Orion-resultaten. De engine doet geen externe AI-call en neemt nooit een
    investeringsbeslissing.
    """

    def __init__(
        self,
        explanation_registry: AIExplanationRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.explanation_registry = explanation_registry or AIExplanationRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def explain(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig | None = None,
    ) -> AIExplanationResult:
        config = explanation_config or AIExplanationConfig()
        explanation_result = AIExplanationResult(
            symbol=explanation_context.resolved_symbol(),
            title=explanation_context.title,
        )

        return self.analyzer_runner.run(
            registry=self.explanation_registry,
            result=explanation_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    explanation_context=explanation_context,
                    explanation_config=config,
                    explanation_result=result,
                )
            ),
        )
