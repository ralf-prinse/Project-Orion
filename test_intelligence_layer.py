from services.intelligence.market_intelligence_engine import MarketIntelligenceEngine
from services.intelligence.intelligence_models import IndicatorPack


def run():
    engine = MarketIntelligenceEngine()

    data = IndicatorPack(
        symbol="TSLA",
        rsi=72,
        trend=0.6,
        volatility=0.4,
        momentum=65,
    )

    result = engine.analyze(data)

    print("\n🧠 MARKET INTELLIGENCE RESULT")
    print("Symbol:", result.symbol)
    print("Score:", result.composite_score)
    print("Regime:", result.regime)
    print("Volatility:", result.volatility_state)
    print("Risk:", result.risk_score)
    print("Confidence:", result.confidence)
    print("Features:", result.ai_feature_vector)


if __name__ == "__main__":
    run()