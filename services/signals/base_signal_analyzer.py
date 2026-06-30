from abc import ABC, abstractmethod

from services.analysis.models import AnalysisResult
from services.signals.models import SignalResult


class BaseSignalAnalyzer(ABC):
    """
    Basisinterface voor alle signal analyzers binnen de Signal Layer.

    Iedere signal analyzer:
    - ontvangt een AnalysisResult
    - vult SignalResult aan met signaalinformatie
    - blijft volledig deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        analysis_result: AnalysisResult,
        signal_result: SignalResult,
    ) -> SignalResult:
        """
        Analyseer een AnalysisResult en verrijk SignalResult.
        """
        raise NotImplementedError