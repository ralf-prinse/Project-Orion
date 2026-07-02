from services.portfolio.analytics_service import PortfolioAnalyticsService
from services.portfolio.models import PortfolioPosition, PortfolioState


def test_empty_portfolio():
    service = PortfolioAnalyticsService()

    state = PortfolioState(
        cash=1000.0,
        positions={},
        currency="USD",
    )

    result = service.analyze(state)

    assert result.cash == 1000.0
    assert result.invested_value == 0.0
    assert result.total_value == 1000.0
    assert result.open_positions == 0
    assert result.total_exposure == 0.0
    assert result.average_position_value == 0.0
    assert result.largest_position_symbol is None
    assert result.largest_position_value == 0.0
    assert result.currency == "USD"


def test_portfolio_with_positions():
    service = PortfolioAnalyticsService()

    state = PortfolioState(
        cash=500.0,
        currency="USD",
        positions={
            "AAPL": PortfolioPosition(
                symbol="AAPL",
                quantity=10,
                average_price=100.0,
                current_price=110.0,
            ),
            "MSFT": PortfolioPosition(
                symbol="MSFT",
                quantity=5,
                average_price=200.0,
                current_price=220.0,
            ),
        },
    )

    result = service.analyze(state)

    assert result.cash == 500.0
    assert result.invested_value == 2200.0
    assert result.total_value == 2700.0
    assert result.open_positions == 2
    assert result.total_exposure == round(2200.0 / 2700.0, 4)
    assert result.average_position_value == 1100.0
    assert result.largest_position_symbol == "AAPL"
    assert result.largest_position_value == 1100.0
    assert result.currency == "USD"