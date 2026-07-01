from dataclasses import dataclass

from services.ai.base_ai_explanation_analyzer import BaseAIExplanationAnalyzer
from services.ai.analyzers.input_validation_analyzer import InputValidationAnalyzer
from services.ai.analyzers.decision_explanation_analyzer import DecisionExplanationAnalyzer
from services.ai.analyzers.trade_plan_explanation_analyzer import TradePlanExplanationAnalyzer
from services.ai.analyzers.performance_explanation_analyzer import PerformanceExplanationAnalyzer
from services.ai.analyzers.explainability_report_analyzer import ExplainabilityReportAnalyzer
from services.ai.analyzers.summary_assembler_analyzer import SummaryAssemblerAnalyzer


@dataclass(frozen=True)
class AIExplanationAnalyzerDefinition:
    """
    Registry-item voor de AI Explanation Layer.
    """

    name: str
    analyzer: BaseAIExplanationAnalyzer


class AIExplanationRegistry:
    """
    Bepaalt de deterministische uitvoervolgorde van AI Explanation analyzers.
    """

    def __init__(self):
        self._analyzers: list[AIExplanationAnalyzerDefinition] = []
        self.register_defaults()

    def register_defaults(self) -> None:
        self._analyzers = [
            AIExplanationAnalyzerDefinition(
                name="input_validation",
                analyzer=InputValidationAnalyzer(),
            ),
            AIExplanationAnalyzerDefinition(
                name="decision_explanation",
                analyzer=DecisionExplanationAnalyzer(),
            ),
            AIExplanationAnalyzerDefinition(
                name="trade_plan_explanation",
                analyzer=TradePlanExplanationAnalyzer(),
            ),
            AIExplanationAnalyzerDefinition(
                name="performance_explanation",
                analyzer=PerformanceExplanationAnalyzer(),
            ),
            AIExplanationAnalyzerDefinition(
                name="explainability_report",
                analyzer=ExplainabilityReportAnalyzer(),
            ),
            AIExplanationAnalyzerDefinition(
                name="summary_assembler",
                analyzer=SummaryAssemblerAnalyzer(),
            ),
        ]

    def register(
        self,
        name: str,
        analyzer: BaseAIExplanationAnalyzer,
    ) -> None:
        self._analyzers.append(
            AIExplanationAnalyzerDefinition(
                name=name,
                analyzer=analyzer,
            )
        )

    def get_analyzers(self) -> list[AIExplanationAnalyzerDefinition]:
        return list(self._analyzers)
