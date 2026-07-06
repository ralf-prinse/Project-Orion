from services.risk.adaptive_risk_engine import AdaptiveRiskEngine


def main():
    engine = AdaptiveRiskEngine()

    plan = engine.build(
        symbol="INGA.AS",
        entry_price=28.50,
        confidence=0.86,
        risk_score=0.0008,
        volatility="LOW",
        regime="BULL",
    )

    assert plan.symbol == "INGA.AS"
    assert plan.entry_price == 28.50
    assert plan.stop_loss < plan.entry_price
    assert plan.target_1 > plan.entry_price
    assert plan.target_2 > plan.target_1
    assert plan.target_3 > plan.target_2
    assert plan.risk_percent > 0
    assert plan.reward_percent > 0
    assert plan.risk_reward_ratio > 1
    assert "Adaptive risk plan" in plan.notes

    invalid_plan = engine.build(
        symbol="TEST",
        entry_price=0,
        confidence=0.5,
        risk_score=0.0,
        volatility="LOW",
        regime="BULL",
    )

    assert invalid_plan.entry_price == 0.0
    assert invalid_plan.stop_loss == 0.0
    assert invalid_plan.target_1 == 0.0

    print("ADAPTIVE RISK ENGINE: PASS ✅")


if __name__ == "__main__":
    main()