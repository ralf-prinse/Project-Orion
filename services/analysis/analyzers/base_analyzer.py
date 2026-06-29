from abc import ABC, abstractmethod

from services.analysis.models import AnalysisResult, IndicatorResult


class BaseAnalyzer(ABC):
    """
    Basisinterface voor alle analyzers binnen de Analysis Layer.

    Iedere analyzer:
    - ontvangt IndicatorResult
    - vult AnalysisResult aan met notes
    - retourneert een score tussen 0 en 100
    """

    @abstractmethod
    def analyze(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        """
        Analyseer indicatoren en retourneer een score tussen 0 en 100.
        """
        raise NotImplementedError