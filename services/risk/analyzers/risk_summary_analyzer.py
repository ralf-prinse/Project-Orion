from services.risk.base_risk_analyzer import BaseRiskAnalyzer
from services.risk.models import RiskContext, RiskProfile, RiskResult


class RiskSummaryAnalyzer(BaseRiskAnalyzer):
    """
    Berekent deterministische risk-samenvatting.
    """

    def analyze(
        self,
        risk_context: RiskContext,
        risk_profile: RiskProfile,
        risk_result: RiskResult,
    ) -> RiskResult:
        risk_result.symbol = risk_context.symbol.upper()
        risk_result.portfolio_value = round(risk_context.portfolio_value, 2)
        risk_result.proposed_risk_ratio = risk_context.proposed_risk_ratio()
        risk_result.total_portfolio_risk = risk_context.total_portfolio_risk()
        risk_result.drawdown = risk_context.drawdown_ratio()
        risk_result.cash_reserve_after_trade = risk_context.cash_reserve_after_trade()
        risk_result.position_exposure = risk_context.proposed_position_exposure()
        risk_result.add_reason("Risk summary calculated.")

        return risk_result
