from services.decisions.base_decision_analyzer import BaseDecisionAnalyzer
from services.decisions.models import DecisionContext, DecisionState
from services.signals.models import SignalResult


class RiskValidationAnalyzer(BaseDecisionAnalyzer):
    """
    Controleert of een beslissing binnen het risicoprofiel past.

    Sprint 8.3.2:
    - gebruikt voorlopig alleen DecisionContext.risk_profile
    - blokkeert wanneer risk_profile gelijk is aan 'blocked'
    - blijft voorbereid op toekomstige Risk Manager-integratie
    """

    def analyze(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext,
        decision_state: DecisionState,
    ) -> DecisionState:
        if decision_context.risk_profile == "blocked":
            decision_state.risk_allowed = False
            decision_state.add_warning(
                "Risk validation blocked decision; risk profile is blocked."
            )
            return decision_state

        decision_state.risk_allowed = True
        decision_state.add_reason("Risk validation passed.")

        return decision_state