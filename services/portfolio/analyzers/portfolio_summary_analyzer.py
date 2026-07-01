from services.portfolio.base_portfolio_analyzer import BasePortfolioAnalyzer
from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState


class PortfolioSummaryAnalyzer(BasePortfolioAnalyzer):
    """
    Berekent deterministische portfolio-samenvatting.

    Deze analyzer meet alleen portefeuillewaarden. Hij beslist niet of een
    trade technisch interessant is.
    """

    def analyze(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext,
        portfolio_result: PortfolioResult,
    ) -> PortfolioResult:
        portfolio_result.portfolio_value = portfolio_state.total_value()
        portfolio_result.cash_available = round(portfolio_state.cash, 2)
        portfolio_result.open_positions = portfolio_state.open_position_count()
        portfolio_result.proposed_position_value = portfolio_context.proposed_position_value()
        portfolio_result.add_reason("Portfolio summary calculated.")

        return portfolio_result
