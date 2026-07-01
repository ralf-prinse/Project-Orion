from services.risk import RiskContext, RiskProfile, RiskResult


def test_risk_context_calculates_proposed_risk_ratio():
    context = RiskContext(
        portfolio_value=10_000,
        proposed_risk_amount=100,
    )

    assert context.proposed_risk_ratio() == 0.01


def test_risk_context_calculates_total_portfolio_risk():
    context = RiskContext(
        portfolio_value=10_000,
        current_portfolio_risk=0.03,
        proposed_risk_amount=100,
    )

    assert context.total_portfolio_risk() == 0.04


def test_risk_context_calculates_drawdown_from_peak():
    context = RiskContext(
        portfolio_value=9_000,
        peak_portfolio_value=10_000,
    )

    assert context.drawdown_ratio() == 0.1


def test_risk_profile_defaults_are_conservative():
    profile = RiskProfile()

    assert profile.max_risk_per_trade == 0.01
    assert profile.max_portfolio_risk == 0.06
    assert profile.max_drawdown == 0.10
    assert profile.min_cash_reserve == 0.10
    assert profile.max_position_exposure == 0.25


def test_risk_result_collects_reasons_and_warnings():
    result = RiskResult(symbol="AAPL")

    result.add_reason("Risk summary calculated.")
    result.add_warning("Risk warning.")

    assert result.reasons == ["Risk summary calculated."]
    assert result.warnings == ["Risk warning."]
