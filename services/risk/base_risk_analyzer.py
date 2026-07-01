from abc import ABC, abstractmethod

from services.risk.models import RiskContext, RiskProfile, RiskResult


class BaseRiskAnalyzer(ABC):
    """
    Basisinterface voor Risk Manager analyzers.

    Iedere risk analyzer:
    - ontvangt RiskContext
    - ontvangt RiskProfile
    - verrijkt RiskResult
    - blijft volledig deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        """
        Analyseer risicocontext en verrijk RiskResult.
        """
        raise NotImplementedError
