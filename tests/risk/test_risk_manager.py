from services.risk import RiskContext, RiskManager, RiskProfile


def test_risk_manager_allows_valid_risk_context():
    manager = RiskManager()
    context = RiskContext(
        symbol="AAPL",
        portfolio_value=10_000,
        cash_available=5_000,
        current_portfolio_risk=0.02,
        proposed_position_value=2_000,
        proposed_risk_amount=100,
        peak_portfolio_value=10_500,
    )
    profile = RiskProfile(
        max_risk_per_trade=0.02,
        max_portfolio_risk=0.06,
        max_drawdown=0.20,
        min_cash_reserve=0.10,
        max_position_exposure=0.25,
    )

    result = manager.evaluate(
        risk_context=context,
        risk_profile=profile,
    )

    assert result.risk_allowed is True
    assert result.symbol == "AAPL"
    assert result.proposed_risk_ratio == 0.01
    assert result.total_portfolio_risk == 0.03
    assert result.drawdown == 0.0476
    assert result.cash_reserve_after_trade == 0.3
    assert result.position_exposure == 0.2
    assert "Risk summary calculated." in result.reasons
    assert "Trade risk validation passed." in result.reasons
    assert "Portfolio risk validation passed." in result.reasons


def test_risk_manager_blocks_trade_risk_limit_exceeded():
    manager = RiskManager()
    context = RiskContext(
        portfolio_value=10_000,
        cash_available=5_000,
        proposed_position_value=1_000,
        proposed_risk_amount=300,
    )
    profile = RiskProfile(max_risk_per_trade=0.02)

    result = manager.evaluate(context, profile)

    assert result.risk_allowed is False
    assert result.trade_risk_allowed is False
    assert (
        "Risk validation blocked proposal; risk per trade limit exceeded."
        in result.warnings
    )


def test_risk_manager_blocks_total_portfolio_risk_limit_exceeded():
    manager = RiskManager()
    context = RiskContext(
        portfolio_value=10_000,
        cash_available=5_000,
        current_portfolio_risk=0.055,
        proposed_position_value=1_000,
        proposed_risk_amount=100,
    )
    profile = RiskProfile(
        max_risk_per_trade=0.02,
        max_portfolio_risk=0.06,
    )

    result = manager.evaluate(context, profile)

    assert result.risk_allowed is False
    assert result.portfolio_risk_allowed is False
    assert result.total_portfolio_risk == 0.065
    assert (
        "Risk validation blocked proposal; total portfolio risk limit exceeded."
        in result.warnings
    )


def test_risk_manager_blocks_drawdown_limit_exceeded():
    manager = RiskManager()
    context = RiskContext(
        portfolio_value=8_000,
        cash_available=5_000,
        proposed_position_value=1_000,
        proposed_risk_amount=80,
        peak_portfolio_value=10_000,
    )
    profile = RiskProfile(max_drawdown=0.10)

    result = manager.evaluate(context, profile)

    assert result.risk_allowed is False
    assert result.drawdown_allowed is False
    assert result.drawdown == 0.2
    assert (
        "Risk validation blocked proposal; maximum drawdown exceeded."
        in result.warnings
    )


def test_risk_manager_blocks_minimum_cash_reserve_violation():
    manager = RiskManager()
    context = RiskContext(
        portfolio_value=10_000,
        cash_available=2_000,
        proposed_position_value=1_500,
        proposed_risk_amount=50,
    )
    profile = RiskProfile(
        max_risk_per_trade=0.02,
        min_cash_reserve=0.10,
    )

    result = manager.evaluate(context, profile)

    assert result.risk_allowed is False
    assert result.capital_protection_allowed is False
    assert result.cash_reserve_after_trade == 0.05
    assert (
        "Risk validation blocked proposal; minimum cash reserve would be violated."
        in result.warnings
    )


def test_risk_manager_blocks_position_exposure_limit_exceeded():
    manager = RiskManager()
    context = RiskContext(
        portfolio_value=10_000,
        cash_available=5_000,
        proposed_position_value=3_000,
        proposed_risk_amount=100,
    )
    profile = RiskProfile(
        max_risk_per_trade=0.02,
        max_position_exposure=0.25,
    )

    result = manager.evaluate(context, profile)

    assert result.risk_allowed is False
    assert result.position_exposure_allowed is False
    assert result.position_exposure == 0.3
    assert (
        "Risk validation blocked proposal; position exposure risk limit exceeded."
        in result.warnings
    )
