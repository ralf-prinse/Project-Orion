from services.decision.decision_engine import DecisionEngine
from services.decision.decision_models import MarketSignal, PositionContext, DecisionInput


def test_decision():
    engine = DecisionEngine()

    signal = MarketSignal(
        symbol="AAPL",
        score=80,
        trend=1,
        volatility=0.2,
        momentum=0.5,
    )

    context = PositionContext(
        cash=10000,
        position_size=0,
        exposure=0,
    )

    decision = engine.evaluate(DecisionInput(signal, context))

    assert decision.decision in ["BUY", "SELL", "HOLD"]
    assert decision.symbol == "AAPL"