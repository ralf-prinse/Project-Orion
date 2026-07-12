from services.strategy.conviction_explainer import ConvictionExplainer


def test_conviction_explainer():

    explainer = ConvictionExplainer()

    strengths, weaknesses = explainer.explain(
        trend=0.92,
        momentum=0.91,
        buy_pressure=0.75,
        volatility=0.45,
        risk_reward=3.1,
        market_regime="BULL",
    )

    assert "Sterke kortetermijntrend" in strengths
    assert "Momentum versnelt" in strengths
    assert "Koopdruk overheerst" in strengths
    assert "Risk/Reward is aantrekkelijk" in strengths
    assert "Bull market ondersteunt trade" in strengths

    assert len(weaknesses) == 0