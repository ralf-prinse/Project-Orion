from services.portfolio import (
    PortfolioContext,
    PortfolioEngine,
    PortfolioPosition,
    PortfolioState,
)


def test_portfolio_engine_allows_valid_proposed_position():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(
        cash=10_000,
        positions={
            "MSFT": PortfolioPosition(
                symbol="MSFT",
                quantity=10,
                average_price=200,
                current_price=200,
            )
        },
    )
    portfolio_context = PortfolioContext(
        symbol="AAPL",
        proposed_shares=20,
        entry_price=100,
        max_positions=5,
        max_position_exposure=0.25,
        max_total_exposure=1.0,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is True
    assert result.portfolio_value == 12000.0
    assert result.cash_available == 10000.0
    assert result.open_positions == 1
    assert result.proposed_position_value == 2000.0
    assert result.position_exposure == 0.1667
    assert result.total_exposure == 0.3333
    assert "Portfolio summary calculated." in result.reasons
    assert "Exposure validation passed." in result.reasons


def test_portfolio_engine_blocks_when_cash_is_insufficient():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(cash=500)
    portfolio_context = PortfolioContext(
        symbol="AAPL",
        proposed_shares=10,
        entry_price=100,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is False
    assert result.cash_sufficient is False
    assert (
        "Portfolio validation blocked proposal; insufficient cash available."
        in result.warnings
    )


def test_portfolio_engine_blocks_when_max_positions_reached():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(
        cash=10_000,
        positions={
            "AAPL": PortfolioPosition("AAPL", 1, 100),
            "MSFT": PortfolioPosition("MSFT", 1, 100),
        },
    )
    portfolio_context = PortfolioContext(
        symbol="NVDA",
        proposed_shares=1,
        entry_price=100,
        max_positions=2,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is False
    assert result.position_limit_allowed is False
    assert (
        "Portfolio validation blocked proposal; maximum positions reached."
        in result.warnings
    )


def test_portfolio_engine_blocks_existing_position_by_default():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(
        cash=10_000,
        positions={
            "AAPL": PortfolioPosition("AAPL", 10, 100),
        },
    )
    portfolio_context = PortfolioContext(
        symbol="AAPL",
        proposed_shares=5,
        entry_price=100,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is False
    assert result.existing_position_allowed is False
    assert (
        "Portfolio validation blocked proposal; symbol already has an open position."
        in result.warnings
    )


def test_portfolio_engine_allows_existing_position_when_configured():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(
        cash=10_000,
        positions={
            "AAPL": PortfolioPosition("AAPL", 10, 100),
        },
    )
    portfolio_context = PortfolioContext(
        symbol="AAPL",
        proposed_shares=5,
        entry_price=100,
        allow_existing_position=True,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is True
    assert result.existing_position_allowed is True


def test_portfolio_engine_blocks_position_exposure_limit():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(cash=10_000)
    portfolio_context = PortfolioContext(
        symbol="AAPL",
        proposed_shares=40,
        entry_price=100,
        max_position_exposure=0.25,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is False
    assert result.exposure_allowed is False
    assert result.position_exposure == 0.4
    assert (
        "Portfolio validation blocked proposal; position exposure limit exceeded."
        in result.warnings
    )


def test_portfolio_engine_blocks_total_exposure_limit():
    engine = PortfolioEngine()
    portfolio_state = PortfolioState(
        cash=1_000,
        positions={
            "MSFT": PortfolioPosition("MSFT", 9, 1_000, 1_000),
        },
    )
    portfolio_context = PortfolioContext(
        symbol="AAPL",
        proposed_shares=5,
        entry_price=100,
        max_position_exposure=1.0,
        max_total_exposure=0.9,
    )

    result = engine.evaluate(
        portfolio_state=portfolio_state,
        portfolio_context=portfolio_context,
    )

    assert result.portfolio_allowed is False
    assert result.exposure_allowed is False
    assert result.total_exposure == 0.95
    assert (
        "Portfolio validation blocked proposal; total exposure limit exceeded."
        in result.warnings
    )
