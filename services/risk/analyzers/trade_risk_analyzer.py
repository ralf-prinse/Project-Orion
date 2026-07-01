from services.risk.base_risk_analyzer import BaseRiskAnalyzer
from services.risk.models import RiskContext, RiskProfile, RiskResult


class TradeRiskAnalyzer(BaseRiskAnalyzer):
    """
    Valideert risico van de voorgestelde trade ten opzichte van portefeuillewaarde.
    """

    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        if risk_context.portfolio_value <= 0:
            risk_result.trade_risk_allowed = False
            risk_result.risk_allowed = False
            risk_result.add_warning(
                "Risk validation blocked proposal; portfolio value is not configured."
            )
            return risk_result

        if risk_context.proposed_risk_amount <= 0:
            risk_result.trade_risk_allowed = True
            risk_result.add_reason(
                "Trade risk validation skipped; no proposed risk amount configured."
            )
            return risk_result

        if (
            risk_profile.max_risk_per_trade > 0
            and risk_result.proposed_risk_ratio > risk_profile.max_risk_per_trade
        ):
            risk_result.trade_risk_allowed = False
            risk_result.risk_allowed = False
            risk_result.add_warning(
                "Risk validation blocked proposal; risk per trade limit exceeded."
            )
            return risk_result

        risk_result.trade_risk_allowed = True
        risk_result.add_reason("Trade risk validation passed.")

        return risk_result
