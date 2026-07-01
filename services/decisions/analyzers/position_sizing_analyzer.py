from math import floor

from services.decisions.base_decision_analyzer import BaseDecisionAnalyzer
from services.decisions.models import (
    DecisionContext,
    DecisionState,
    PositionSizingResult,
)
from services.signals.models import Signal, SignalResult


class PositionSizingAnalyzer(BaseDecisionAnalyzer):
    """
    Berekent een deterministische aanbevolen positiegrootte.

    Deze analyzer:
    - gebruikt fixed-fractional risk sizing
    - verrijkt uitsluitend DecisionState
    - beslist niet of een positie geopend mag worden
    - bevat geen portfolio management of trade planning
    """

    ACTIONABLE_SIGNALS = {
        Signal.BUY,
        Signal.WATCH,
    }

    def analyze(
        self,
        signal_result: SignalResult,
        decision_context: DecisionContext,
        decision_state: DecisionState,
    ) -> DecisionState:
        sizing_result = PositionSizingResult()
        decision_state.position_sizing = sizing_result
        decision_state.position_size = 0.0

        if not decision_state.signal_valid:
            self._add_warning(
                decision_state=decision_state,
                sizing_result=sizing_result,
                warning="Position sizing skipped because signal is invalid.",
            )
            return decision_state

        if not decision_state.portfolio_allowed:
            self._add_warning(
                decision_state=decision_state,
                sizing_result=sizing_result,
                warning="Position sizing skipped because portfolio rules blocked the decision.",
            )
            return decision_state

        if not decision_state.risk_allowed:
            self._add_warning(
                decision_state=decision_state,
                sizing_result=sizing_result,
                warning="Position sizing skipped because risk rules blocked the decision.",
            )
            return decision_state

        if signal_result.signal not in self.ACTIONABLE_SIGNALS:
            self._add_warning(
                decision_state=decision_state,
                sizing_result=sizing_result,
                warning=(
                    "Position sizing skipped because signal does not require "
                    "a new long position."
                ),
            )
            return decision_state

        validation_warning = self._validate_context(decision_context)
        if validation_warning:
            self._add_warning(
                decision_state=decision_state,
                sizing_result=sizing_result,
                warning=validation_warning,
            )
            return decision_state

        account_equity = self._get_account_equity(decision_context)
        risk_amount = account_equity * decision_context.risk_per_trade
        risk_per_share = decision_context.entry_price - decision_context.stop_loss
        recommended_shares = floor(risk_amount / risk_per_share)

        if decision_context.max_position_value > 0:
            max_affordable_shares = floor(
                decision_context.max_position_value / decision_context.entry_price
            )
            recommended_shares = min(recommended_shares, max_affordable_shares)

        if decision_context.available_cash > 0:
            cash_affordable_shares = floor(
                decision_context.available_cash / decision_context.entry_price
            )
            recommended_shares = min(recommended_shares, cash_affordable_shares)

        position_value = recommended_shares * decision_context.entry_price
        capital_used = position_value

        sizing_result.recommended_shares = recommended_shares
        sizing_result.position_value = round(position_value, 2)
        sizing_result.risk_amount = round(risk_amount, 2)
        sizing_result.risk_per_share = round(risk_per_share, 2)
        sizing_result.capital_used = round(capital_used, 2)

        decision_state.position_size = float(recommended_shares)
        decision_state.add_reason(
            "Position sizing calculated using fixed fractional risk model."
        )

        if recommended_shares <= 0:
            self._add_warning(
                decision_state=decision_state,
                sizing_result=sizing_result,
                warning="Position sizing produced zero shares.",
            )

        return decision_state

    def _validate_context(
        self,
        decision_context: DecisionContext,
    ) -> str | None:
        account_equity = self._get_account_equity(decision_context)

        if account_equity <= 0:
            return "Position sizing skipped; account equity is not configured."

        if decision_context.risk_per_trade <= 0:
            return "Position sizing skipped; risk per trade must be greater than zero."

        if decision_context.entry_price <= 0:
            return "Position sizing skipped; entry price must be greater than zero."

        if decision_context.stop_loss <= 0:
            return "Position sizing skipped; stop loss must be greater than zero."

        if decision_context.stop_loss >= decision_context.entry_price:
            return "Position sizing skipped; stop loss must be below entry price."

        return None

    def _get_account_equity(
        self,
        decision_context: DecisionContext,
    ) -> float:
        if decision_context.portfolio_value > 0:
            return decision_context.portfolio_value

        return decision_context.available_cash

    def _add_warning(
        self,
        decision_state: DecisionState,
        sizing_result: PositionSizingResult,
        warning: str,
    ):
        decision_state.add_warning(warning)
        sizing_result.add_warning(warning)
