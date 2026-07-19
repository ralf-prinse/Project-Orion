from services.trading_decision import AdaptiveDecisionEngine, MarketSignal


def run():
    print("🧪 Starting decision smoke test...")

    engine = AdaptiveDecisionEngine()

    signal = MarketSignal(
        symbol="BTC",
        score=0.75,
        trend=1.0,
        volatility=0.30,
        momentum=0.60,
    )

    result = engine.evaluate(signal)

    print("\nRESULT")
    print("----------------------------")
    print(f"Decision   : {result.decision}")
    print(f"Confidence : {result.confidence:.3f}")
    print(f"Reason     : {result.reason}")

    print("\n✅ Decision smoke test completed")


if __name__ == "__main__":
    run()
