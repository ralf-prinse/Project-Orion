from services.portfolio.base_portfolio_analyzer import BasePortfolioAnalyzer
from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState


class PositionCountAnalyzer(BasePortfolioAnalyzer):
    """
    Valideert het maximum aantal open posities.
    """

    def analyze(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext,
        portfolio_result: PortfolioResult,
    ) -> PortfolioResult:
        if portfolio_context.max_positions <= 0:
            portfolio_result.position_limit_allowed = True
            portfolio_result.add_reason(
                "Position count validation skipped; no max position limit configured."
            )
            return portfolio_result

        if portfolio_state.open_position_count() >= portfolio_context.max_positions:
            portfolio_result.position_limit_allowed = False
            portfolio_result.portfolio_allowed = False
            portfolio_result.add_warning(
                "Portfolio validation blocked proposal; maximum positions reached."
            )
            return portfolio_result

        portfolio_result.position_limit_allowed = True
        portfolio_result.add_reason("Position count validation passed.")

        return portfolio_result
