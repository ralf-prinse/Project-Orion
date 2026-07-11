from services.intelligence.intelligence_models import IndicatorPack
from services.orchestration.trading_pipeline import TradingPipeline


class FakePortfolio:
    cash = 10000.0
    position_size = 0.0
    exposure = 0.0


def run():
    result = TradingPipeline().run(
        IndicatorPack(
            symbol="ORION",
            rsi=64.0,
            trend=0.7,
            volatility=30.0,
            momentum=70.0,
            volume=100000.0,
            price=100.0,
        ),
        FakePortfolio(),
    )

    thesis = result.investment_thesis

    assert thesis is not None
    assert thesis.symbol == "ORION"
    assert thesis.stance in {"BUY", "WATCH", "AVOID"}
    assert 0.0 <= thesis.conviction <= 100.0
    assert len(thesis.factors) == 7

    # Shadow mode: the existing deterministic decision contract stays intact.
    assert result.decision in {"BUY", "HOLD", "SELL"}

    print("STRATEGY THESIS PIPELINE: PASS ✅")


if __name__ == "__main__":
    run()
