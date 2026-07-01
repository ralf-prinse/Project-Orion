from services.risk.base_risk_analyzer import BaseRiskAnalyzer
from services.risk.models import RiskContext, RiskProfile, RiskResult


class PortfolioRiskAnalyzer(BaseRiskAnalyzer):
    """
    Valideert totale portefeuille-risk na de voorgestelde trade.
    """

    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        if (
            risk_profile.max_portfolio_risk > 0
            and risk_result.total_portfolio_risk > risk_profile.max_portfolio_risk
        ):
            risk_result.portfolio_risk_allowed = False
            risk_result.risk_allowed = False
            risk_result.add_warning(
                "Risk validation blocked proposal; total portfolio risk limit exceeded."
            )
            return risk_result

        risk_result.portfolio_risk_allowed = True
        risk_result.add_reason("Portfolio risk validation passed.")

        return risk_result
