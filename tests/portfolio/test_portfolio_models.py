from services.portfolio.models import PortfolioPosition, PortfolioState


def test_portfolio_position_calculates_market_value_from_current_price():
    position = PortfolioPosition(
        symbol="AAPL",
        quantity=10,
        average_price=100,
        current_price=125,
    )

    assert position.market_value() == 1250.0


def test_portfolio_state_calculates_total_values_and_open_positions():
    portfolio_state = PortfolioState(
        cash=5_000,
        positions={
            "AAPL": PortfolioPosition(
                symbol="AAPL",
                quantity=10,
                average_price=100,
                current_price=120,
            ),
            "MSFT": PortfolioPosition(
                symbol="MSFT",
                quantity=5,
                average_price=200,
                current_price=210,
            ),
        },
    )

    assert portfolio_state.total_position_value() == 2250.0
    assert portfolio_state.total_value() == 7250.0
    assert portfolio_state.open_position_count() == 2
    assert portfolio_state.has_position("aapl") is True
    assert portfolio_state.has_position("NVDA") is False
