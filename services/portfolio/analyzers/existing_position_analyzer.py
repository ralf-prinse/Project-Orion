from services.portfolio.base_portfolio_analyzer import BasePortfolioAnalyzer
from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState


class ExistingPositionAnalyzer(BasePortfolioAnalyzer):
    """
    Controleert of een voorgestelde nieuwe positie al bestaat.
    """

    def analyze(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext,
        portfolio_result: PortfolioResult,
    ) -> PortfolioResult:
        symbol = portfolio_context.symbol.upper()

        if not symbol:
            portfolio_result.existing_position_allowed = True
            portfolio_result.add_reason(
                "Existing position validation skipped; no symbol configured."
            )
            return portfolio_result

        if portfolio_context.allow_existing_position:
            portfolio_result.existing_position_allowed = True
            portfolio_result.add_reason(
                "Existing position validation skipped; adding to existing positions is allowed."
            )
            return portfolio_result

        if portfolio_state.has_position(symbol):
            portfolio_result.existing_position_allowed = False
            portfolio_result.portfolio_allowed = False
            portfolio_result.add_warning(
                "Portfolio validation blocked proposal; symbol already has an open position."
            )
            return portfolio_result

        portfolio_result.existing_position_allowed = True
        portfolio_result.add_reason("Existing position validation passed.")

        return portfolio_result
