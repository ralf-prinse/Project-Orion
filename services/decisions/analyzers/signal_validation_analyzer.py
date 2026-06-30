from services.decisions.base_decision_analyzer import BaseDecisionAnalyzer
from services.decisions.models import DecisionContext, DecisionState
from services.signals.models import Signal, SignalResult


class SignalValidationAnalyzer(BaseDecisionAnalyzer):
    """
    Valideert of een technisch signaal bruikbaar is voor besluitvorming.

    Sprint 8.3.1:
    - BUY, WATCH, HOLD en SELL worden als geldige signalen beschouwd.
    - IGNORE wordt niet als actionable signaal beschouwd.
    """

    def analyze(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext,
        decision_state: DecisionState,
    ) -> DecisionState:
        if signal_result.signal == Signal.IGNORE:
            decision_state.signal_valid = False
            decision_state.add_warning("Signal is IGNORE; no decision action allowed.")
            return decision_state

        decision_state.signal_valid = True
        decision_state.confidence = signal_result.confidence
        decision_state.add_reason(f"Signal {signal_result.signal.value} is valid.")

        return decision_state