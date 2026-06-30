from services.decisions.base_decision_analyzer import BaseDecisionAnalyzer
from services.decisions.models import DecisionContext, DecisionState
from services.signals.models import SignalResult


class PortfolioValidationAnalyzer(BaseDecisionAnalyzer):
    """
    Controleert of een nieuwe beslissing binnen de portefeuillecapaciteit past.

    Sprint 8.3.2:
    - gebruikt alleen DecisionContext
    - blokkeert nieuwe beslissingen wanneer max_positions is bereikt
    - blijft voorbereid op toekomstige Portfolio Engine-integratie
    """

    def analyze(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext,
        decision_state: DecisionState,
    ) -> DecisionState:
        if decision_context.max_positions <= 0:
            decision_state.portfolio_allowed = True
            decision_state.add_reason(
                "Portfolio validation skipped; no max position limit configured."
            )
            return decision_state

        if decision_context.open_positions >= decision_context.max_positions:
            decision_state.portfolio_allowed = False
            decision_state.add_warning(
                "Portfolio validation blocked decision; maximum positions reached."
            )
            return decision_state

        decision_state.portfolio_allowed = True
        decision_state.add_reason("Portfolio validation passed.")

        return decision_state