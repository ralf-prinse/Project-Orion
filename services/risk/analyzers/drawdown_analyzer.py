from services.risk.base_risk_analyzer import BaseRiskAnalyzer
from services.risk.models import RiskContext, RiskProfile, RiskResult


class DrawdownAnalyzer(BaseRiskAnalyzer):
    """
    Valideert of actuele drawdown binnen het risicoprofiel past.
    """

    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        if risk_profile.max_drawdown <= 0:
            risk_result.drawdown_allowed = True
            risk_result.add_reason(
                "Drawdown validation skipped; no max drawdown configured."
            )
            return risk_result

        if risk_result.drawdown > risk_profile.max_drawdown:
            risk_result.drawdown_allowed = False
            risk_result.risk_allowed = False
            risk_result.add_warning(
                "Risk validation blocked proposal; maximum drawdown exceeded."
            )
            return risk_result

        risk_result.drawdown_allowed = True
        risk_result.add_reason("Drawdown validation passed.")

        return risk_result
