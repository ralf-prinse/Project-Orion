from services.risk.base_risk_analyzer import BaseRiskAnalyzer
from services.risk.models import RiskContext, RiskProfile, RiskResult


class CapitalProtectionAnalyzer(BaseRiskAnalyzer):
    """
    Bewaakt minimale cashreserve na een voorgestelde trade.
    """

    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        if risk_context.proposed_position_value <= 0:
            risk_result.capital_protection_allowed = True
            risk_result.add_reason(
                "Capital protection validation skipped; no proposed position value configured."
            )
            return risk_result

        if (
            risk_profile.min_cash_reserve > 0
            and risk_result.cash_reserve_after_trade < risk_profile.min_cash_reserve
        ):
            risk_result.capital_protection_allowed = False
            risk_result.risk_allowed = False
            risk_result.add_warning(
                "Risk validation blocked proposal; minimum cash reserve would be violated."
            )
            return risk_result

        risk_result.capital_protection_allowed = True
        risk_result.add_reason("Capital protection validation passed.")

        return risk_result
