from services.intelligence.intelligence_models import IndicatorPack
from services.orchestration.trading_pipeline import TradingPipeline


class FakePortfolio:
    cash = 10000
    position_size = 0
    exposure = 0


def run():
    pipeline = TradingPipeline()

    indicators = IndicatorPack(
        symbol="TSLA",
        rsi=72,
        trend=0.6,
        volatility=0.25,
        momentum=68,
        volume=1000,
    )

    result = pipeline.run(indicators, FakePortfolio())

    assert result.symbol == "TSLA"
    assert result.decision in {"BUY", "HOLD", "SELL"}
    assert result.confidence >= 0
    assert result.position_size >= 0
    assert result.expected_risk >= 0
    assert result.risk_plan.symbol == "TSLA"
    assert result.risk_plan.entry_price > 0
    assert result.ai_context is not None
    assert result.explanation is not None

    print("TRADING PIPELINE: PASS ✅")


if __name__ == "__main__":
    run()