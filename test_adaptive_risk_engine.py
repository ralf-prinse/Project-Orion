from models.market_structure import MarketStructure
from models.risk_context import RiskContext
from services.risk.adaptive_risk_engine import AdaptiveRiskEngine


def main():
    engine = AdaptiveRiskEngine()

    context = RiskContext(
        symbol="INGA.AS",
        entry_price=28.50,
        confidence=0.86,
        risk_score=0.0008,
        volatility="LOW",
        regime="BULL",
        market_structure=MarketStructure(
            atr=0.45,
            average_range=0.65,
            swing_high=29.20,
            swing_low=27.80,
            resistance=29.20,
            support=27.80,
        ),
    )

    plan = engine.build(context)

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

    invalid_context = RiskContext(
        symbol="TEST",
        entry_price=0,
        confidence=0.5,
        risk_score=0.0,
        volatility="LOW",
        regime="BULL",
        market_structure=MarketStructure(),
    )

    invalid_plan = engine.build(invalid_context)

    assert invalid_plan.entry_price == 0.0
    assert invalid_plan.stop_loss == 0.0
    assert invalid_plan.target_1 == 0.0

    print("ADAPTIVE RISK ENGINE: PASS ✅")


if __name__ == "__main__":
    main()