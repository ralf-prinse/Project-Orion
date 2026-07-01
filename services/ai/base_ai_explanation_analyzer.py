from abc import ABC, abstractmethod

from services.ai.models import (
    AIExplanationConfig,
    AIExplanationContext,
    AIExplanationResult,
)


class BaseAIExplanationAnalyzer(ABC):
    """
    Basisklasse voor AI Explanation analyzers.

    Analyzers verrijken uitsluitend AIExplanationResult op basis van bestaande
    deterministische Orion-output. Zij mogen geen tradinglogica uitvoeren.
    """

    @abstractmethod
    def analyze(
        self,
        explanation_context: AIExplanationContext,
        explanation_config: AIExplanationConfig,
        explanation_result: AIExplanationResult,
    ) -> AIExplanationResult:
        raise NotImplementedError
