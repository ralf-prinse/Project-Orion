from models.portfolio import Portfolio, Position
from services.portfolio.portfolio_state_adapter import PortfolioStateAdapter


def test_adapter_converts_empty_portfolio():
    adapter = PortfolioStateAdapter()

    portfolio = Portfolio(
        cash=1000.0,
        currency="EUR",
        max_position_percentage=0.35,
        positions={},
    )

    state = adapter.from_portfolio(portfolio)

    assert state.cash == 1000.0
    assert state.currency == "EUR"
    assert state.positions == {}


def test_adapter_converts_position_objects():
    adapter = PortfolioStateAdapter()

    portfolio = Portfolio(
        cash=500.0,
        currency="EUR",
        positions={
            "aapl": Position(
                symbol="aapl",
                quantity=3,
                average_price=100.0,
                currency="EUR",
            )
        },
    )

    state = adapter.from_portfolio(portfolio)

    assert state.cash == 500.0
    assert state.currency == "EUR"
    assert "AAPL" in state.positions

    position = state.positions["AAPL"]

    assert position.symbol == "AAPL"
    assert position.quantity == 3
    assert position.average_price == 100.0
    assert position.current_price == 100.0


def test_adapter_converts_serialized_position_dicts():
    adapter = PortfolioStateAdapter()

    portfolio = Portfolio(
        cash=250.0,
        currency="USD",
        positions={
            "msft": {
                "symbol": "msft",
                "quantity": 2,
                "average_price": 200.0,
                "currency": "USD",
            }
        },
    )

    state = adapter.from_portfolio(portfolio)

    assert state.cash == 250.0
    assert state.currency == "USD"
    assert "MSFT" in state.positions

    position = state.positions["MSFT"]

    assert position.symbol == "MSFT"
    assert position.quantity == 2
    assert position.average_price == 200.0
    assert position.current_price == 200.0