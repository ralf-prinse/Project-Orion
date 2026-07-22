import pandas as pd

from models.paper_portfolio import PaperPortfolio
from services.intelligence.indicator_builder import IndicatorBuilder
from services.paper_trading_pipeline_adapter import PaperTradingPipelineAdapter


def test_trend_is_signed_instead_of_always_strongly_bullish() -> None:
    builder = IndicatorBuilder()
    rising = pd.Series([100.0 + index for index in range(40)])
    falling = pd.Series([140.0 - index for index in range(40)])
    flat = pd.Series([100.0] * 40)

    assert builder._calculate_trend(rising) > 0
    assert builder._calculate_trend(falling) < 0
    assert builder._calculate_trend(flat) == 0


def test_volatility_is_annualized_percentage_for_downstream_normalization() -> None:
    builder = IndicatorBuilder()
    close = pd.Series(
        [100.0, 102.0, 99.0, 103.0, 98.0] * 10,
        dtype=float,
    )

    volatility = builder._calculate_volatility(close)

    assert 1.0 < volatility <= 100.0


def test_falling_market_no_longer_produces_structural_buy_bias() -> None:
    adapter = PaperTradingPipelineAdapter()
    rising = adapter.run(
        symbol="RISING",
        history=_history([100.0 + index for index in range(60)]),
        portfolio_state=PaperPortfolio(cash=10_000.0),
    )
    falling = adapter.run(
        symbol="FALLING",
        history=_history([160.0 - index for index in range(60)]),
        portfolio_state=PaperPortfolio(cash=10_000.0),
    )

    assert rising.decision == "BUY"
    assert falling.decision != "BUY"
    assert falling.market_intelligence.regime == "BEAR"


def _history(closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Open": [value - 0.25 for value in closes],
            "High": [value + 1.0 for value in closes],
            "Low": [value - 1.0 for value in closes],
            "Close": closes,
            "Volume": [100_000.0] * len(closes),
        }
    )
