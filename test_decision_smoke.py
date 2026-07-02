from services.decision.decision_models import MarketSignal, PositionContext, DecisionInput
from services.decision.decision_engine import DecisionEngine


def run():
    print("🧪 Starting smoke test...")

    engine = DecisionEngine()

    signal = MarketSignal(
        symbol="BTC",
        score=75,
        trend=1,
        volatility=0.3,
        momentum=0.6,
    )

    context = PositionContext(
        cash=10000,
        position_size=0,
        exposure=0,
    )

    input_data = DecisionInput(signal=signal, context=context)

    result = engine.evaluate(input_data)

    print("RESULT:")
    print(result)

    print("\nDecision:", result.decision)
    print("Confidence:", result.confidence)
    print("Position size:", result.position_size)

    print("\n✅ Smoke test completed")


if __name__ == "__main__":
    run()