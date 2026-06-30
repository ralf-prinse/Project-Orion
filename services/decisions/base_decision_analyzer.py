from abc import ABC, abstractmethod

from services.decisions.models import DecisionContext, DecisionState
from services.signals.models import SignalResult


class BaseDecisionAnalyzer(ABC):
    """
    Basisinterface voor alle decision analyzers binnen Project Orion.

    Iedere decision analyzer:
    - ontvangt SignalResult
    - ontvangt DecisionContext
    - verrijkt DecisionState
    - blijft volledig deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext,
        decision_state: DecisionState,
    ) -> DecisionState:
        """
        Analyseer signaal en context en verrijk DecisionState.
        """
        raise NotImplementedError