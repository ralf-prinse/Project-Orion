from services.trading_decision import AdaptiveDecisionEngine
from services.trading_decision.decision_models import MarketSignal


def test_sell_confidence_is_capped_at_one_for_negative_scores():
    decision = AdaptiveDecisionEngine().evaluate(
        MarketSignal(
            symbol="TEST",
            score=-0.25,
            trend=-0.5,
            volatility=0.4,
            momentum=0.2,
        )
    )

    assert decision.decision == "SELL"
    assert decision.confidence == 1.0
