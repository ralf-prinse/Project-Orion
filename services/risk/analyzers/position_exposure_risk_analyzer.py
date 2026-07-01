from services.risk.base_risk_analyzer import BaseRiskAnalyzer
from services.risk.models import RiskContext, RiskProfile, RiskResult


class PositionExposureRiskAnalyzer(BaseRiskAnalyzer):
    """
    Valideert positie-exposure vanuit risk-perspectief.
    """

    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        if risk_context.proposed_position_value <= 0:
            risk_result.position_exposure_allowed = True
            risk_result.add_reason(
                "Position exposure risk validation skipped; no proposed position value configured."
            )
            return risk_result

        if (
            risk_profile.max_position_exposure > 0
            and risk_result.position_exposure > risk_profile.max_position_exposure
        ):
            risk_result.position_exposure_allowed = False
            risk_result.risk_allowed = False
            risk_result.add_warning(
                "Risk validation blocked proposal; position exposure risk limit exceeded."
            )
            return risk_result

        risk_result.position_exposure_allowed = True
        risk_result.add_reason("Position exposure risk validation passed.")

        return risk_result
