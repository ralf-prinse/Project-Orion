from services.portfolio.base_portfolio_analyzer import BasePortfolioAnalyzer
from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState


class ExposureAnalyzer(BasePortfolioAnalyzer):
    """
    Berekent en valideert positie- en totale portefeuille-exposure.
    """

    def analyze(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext,
        portfolio_result: PortfolioResult,
    ) -> PortfolioResult:
        portfolio_value = portfolio_state.total_value()
        current_position_value = portfolio_state.total_position_value()
        proposed_position_value = portfolio_context.proposed_position_value()

        if portfolio_value <= 0:
            portfolio_result.position_exposure = 0.0
            portfolio_result.total_exposure = 0.0
            portfolio_result.exposure_allowed = False
            portfolio_result.portfolio_allowed = False
            portfolio_result.add_warning(
                "Portfolio validation blocked proposal; portfolio value is not configured."
            )
            return portfolio_result

        portfolio_result.position_exposure = round(
            proposed_position_value / portfolio_value,
            4,
        )
        portfolio_result.total_exposure = round(
            (current_position_value + proposed_position_value) / portfolio_value,
            4,
        )

        if (
            portfolio_context.max_position_exposure > 0
            and portfolio_result.position_exposure > portfolio_context.max_position_exposure
        ):
            portfolio_result.exposure_allowed = False
            portfolio_result.portfolio_allowed = False
            portfolio_result.add_warning(
                "Portfolio validation blocked proposal; position exposure limit exceeded."
            )
            return portfolio_result

        if (
            portfolio_context.max_total_exposure > 0
            and portfolio_result.total_exposure > portfolio_context.max_total_exposure
        ):
            portfolio_result.exposure_allowed = False
            portfolio_result.portfolio_allowed = False
            portfolio_result.add_warning(
                "Portfolio validation blocked proposal; total exposure limit exceeded."
            )
            return portfolio_result

        portfolio_result.exposure_allowed = True
        portfolio_result.add_reason("Exposure validation passed.")

        return portfolio_result
