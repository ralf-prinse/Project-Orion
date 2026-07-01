from services.portfolio.base_portfolio_analyzer import BasePortfolioAnalyzer
from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState


class CashValidationAnalyzer(BasePortfolioAnalyzer):
    """
    Valideert of er voldoende cash beschikbaar is voor de voorgestelde positie.
    """

    def analyze(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext,
        portfolio_result: PortfolioResult,
    ) -> PortfolioResult:
        proposed_value = portfolio_context.proposed_position_value()

        if proposed_value <= 0:
            portfolio_result.cash_sufficient = True
            portfolio_result.add_reason(
                "Cash validation skipped; no proposed position value configured."
            )
            return portfolio_result

        if proposed_value > portfolio_state.cash:
            portfolio_result.cash_sufficient = False
            portfolio_result.portfolio_allowed = False
            portfolio_result.add_warning(
                "Portfolio validation blocked proposal; insufficient cash available."
            )
            return portfolio_result

        portfolio_result.cash_sufficient = True
        portfolio_result.add_reason("Cash validation passed.")

        return portfolio_result
