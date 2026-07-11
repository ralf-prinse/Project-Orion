from models.market_structure import MarketStructure
from models.risk_plan import RiskPlan
from services.intelligence.investment_thesis_builder import (
    InvestmentThesisBuilder,
)
from services.intelligence.intelligence_models import (
    IndicatorPack,
    MarketIntelligenceSnapshot,
)
from services.intelligence.signal_fusion_engine import FusedSignal


def build_risk_plan(ratio: float = 2.5) -> RiskPlan:
    return RiskPlan(
        symbol="TEST",
        entry_price=100.0,
        stop_loss=95.0,
        target_1=112.5,
        target_2=120.0,
        target_3=128.0,
        risk_percent=5.0,
        reward_percent=12.5,
        risk_reward_ratio=ratio,
        confidence=0.8,
        notes="Test plan",
    )


def run():
    builder = InvestmentThesisBuilder()

    bullish = builder.build(
        indicators=IndicatorPack(
            symbol="TEST",
            rsi=62.0,
            trend=0.8,
            volatility=35.0,
            momentum=72.0,
            price=100.0,
            market_structure=MarketStructure(support=94.0),
        ),
        fused=FusedSignal(
            pressure_score=0.75,
            buy_pressure=0.82,
            sell_pressure=0.18,
            strength=0.64,
            trend=0.8,
            momentum=0.72,
            rsi=0.62,
            volatility=0.35,
        ),
        intelligence=MarketIntelligenceSnapshot(
            symbol="TEST",
            composite_score=0.75,
            confidence=0.8,
            regime="BULL",
            volatility_state="MEDIUM",
            trend_strength=0.8,
            momentum_strength=0.72,
            risk_score=0.2,
            ai_feature_vector=[],
        ),
        risk_plan=build_risk_plan(),
    )

    assert bullish.stance == "BUY"
    assert bullish.conviction >= 68.0
    assert len(bullish.factors) == 7
    assert bullish.supporting_reasons
    assert any("support" in item.lower() for item in bullish.invalidation_conditions)

    overextended = builder.build(
        indicators=IndicatorPack(
            symbol="TEST",
            rsi=86.0,
            trend=0.2,
            volatility=85.0,
            momentum=35.0,
            price=100.0,
        ),
        fused=FusedSignal(
            pressure_score=0.2,
            buy_pressure=0.35,
            sell_pressure=0.55,
            strength=0.20,
            trend=0.2,
            momentum=0.35,
            rsi=0.86,
            volatility=0.85,
        ),
        intelligence=MarketIntelligenceSnapshot(
            symbol="TEST",
            composite_score=0.2,
            confidence=0.3,
            regime="SIDEWAYS",
            volatility_state="HIGH",
            trend_strength=0.2,
            momentum_strength=0.35,
            risk_score=0.8,
            ai_feature_vector=[],
        ),
        risk_plan=build_risk_plan(ratio=0.8),
    )

    assert overextended.stance == "AVOID"
    assert any("overextension" in item.lower() for item in overextended.risk_reasons)

    print("INVESTMENT THESIS BUILDER: PASS ✅")


if __name__ == "__main__":
    run()
