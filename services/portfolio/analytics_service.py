from services.portfolio.analytics_models import PortfolioAnalyticsResult
from services.portfolio.models import PortfolioState


class PortfolioAnalyticsService:
    """
    Calculates deterministic portfolio analytics.

    The service consumes PortfolioState and returns portfolio KPI results.
    It does not mutate portfolio state and contains no presentation logic.
    """

    def analyze(self, portfolio_state: PortfolioState) -> PortfolioAnalyticsResult:
        invested_value = portfolio_state.total_position_value()
        total_value = portfolio_state.total_value()
        open_positions = portfolio_state.open_position_count()

        total_exposure = 0.0
        if total_value > 0:
            total_exposure = round(invested_value / total_value, 4)

        average_position_value = 0.0
        if open_positions > 0:
            average_position_value = round(invested_value / open_positions, 2)

        largest_position_symbol = None
        largest_position_value = 0.0

        for symbol, position in portfolio_state.positions.items():
            market_value = position.market_value()

            if market_value > largest_position_value:
                largest_position_symbol = symbol
                largest_position_value = market_value

        return PortfolioAnalyticsResult(
            cash=round(portfolio_state.cash, 2),
            invested_value=round(invested_value, 2),
            total_value=round(total_value, 2),
            open_positions=open_positions,
            total_exposure=total_exposure,
            average_position_value=average_position_value,
            largest_position_symbol=largest_position_symbol,
            largest_position_value=round(largest_position_value, 2),
            currency=portfolio_state.currency,
        )