from services.decisions.base_decision_analyzer import BaseDecisionAnalyzer
from services.decisions.models import (
    DecisionAction,
    DecisionContext,
    DecisionState,
)
from services.signals.models import Signal, SignalResult


class DecisionAssemblerAnalyzer(BaseDecisionAnalyzer):
    """
    Zet de opgebouwde DecisionState om naar een voorgestelde eindactie.

    Deze analyzer beslist alleen op basis van reeds gevalideerde state.
    Portfolio- en risicocontroles blijven aparte analyzers.
    """

    def analyze(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext,
        decision_state: DecisionState,
    ) -> DecisionState:
        if not decision_state.signal_valid:
            decision_state.proposed_action = DecisionAction.SKIP
            decision_state.confidence = 0
            decision_state.add_warning("Decision skipped because signal is invalid.")
            return decision_state

        if not decision_state.portfolio_allowed:
            decision_state.proposed_action = DecisionAction.SKIP
            decision_state.add_warning("Decision skipped because portfolio rules blocked it.")
            return decision_state

        if not decision_state.risk_allowed:
            decision_state.proposed_action = DecisionAction.SKIP
            decision_state.add_warning("Decision skipped because risk rules blocked it.")
            return decision_state

        decision_state.proposed_action = self._map_signal_to_decision_action(
            signal_result.signal
        )
        decision_state.add_reason(
            f"Decision action assembled as {decision_state.proposed_action.value}."
        )

        return decision_state

    def _map_signal_to_decision_action(
        self,
        signal: Signal,
    ) -> DecisionAction:
        if signal == Signal.BUY:
            return DecisionAction.BUY

        if signal == Signal.WATCH:
            return DecisionAction.WATCH

        if signal == Signal.HOLD:
            return DecisionAction.HOLD

        if signal == Signal.SELL:
            return DecisionAction.SELL

        return DecisionAction.SKIP