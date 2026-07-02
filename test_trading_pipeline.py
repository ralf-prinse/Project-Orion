from services.orchestration.trading_pipeline import TradingPipeline
from services.intelligence.intelligence_models import IndicatorPack


class FakePortfolio:
    cash = 10000
    position_size = 0
    exposure = 0


def run():
    pipeline = TradingPipeline()

    # test input (realistic market data)
    indicators = IndicatorPack(
        symbol="TSLA",
        rsi=72,
        trend=0.6,
        volatility=0.25,
        momentum=68,
        volume=1000,
    )

    result = pipeline.run(indicators, FakePortfolio())

    print("\n🚀 FULL PIPELINE RESULT")

    # clean output printing
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    run()