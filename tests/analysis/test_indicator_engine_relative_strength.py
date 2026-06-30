import pandas as pd

from services.analysis.indicator_engine import IndicatorEngine


def _build_candles(close_values):
    return pd.DataFrame(
        {
            "Open": close_values,
            "High": close_values,
            "Low": close_values,
            "Close": close_values,
            "Volume": [1000000] * len(close_values),
        }
    )


def test_indicator_engine_calculates_relative_strength_values():
    stock_candles = _build_candles([100] * 31 + [110] * 20)
    benchmark_candles = _build_candles([100] * 31 + [105] * 20)

    result = IndicatorEngine().calculate(
        symbol="TEST",
        candles=stock_candles,
        benchmark_candles=benchmark_candles,
    )

    assert result.has("relative_strength_20")
    assert result.has("relative_strength_50")
    assert result.has("relative_strength_trend")

    assert round(result.get("relative_strength_20"), 2) == 5.0
    assert round(result.get("relative_strength_50"), 2) == 5.0
    assert round(result.get("relative_strength_trend"), 2) == 0.0


def test_indicator_engine_skips_relative_strength_without_benchmark():
    stock_candles = _build_candles([100] * 60)

    result = IndicatorEngine().calculate(
        symbol="TEST",
        candles=stock_candles,
    )

    assert not result.has("relative_strength_20")
    assert not result.has("relative_strength_50")
    assert not result.has("relative_strength_trend")


def test_indicator_engine_skips_relative_strength_with_short_benchmark_data():
    stock_candles = _build_candles([100] * 60)
    benchmark_candles = _build_candles([100] * 20)

    result = IndicatorEngine().calculate(
        symbol="TEST",
        candles=stock_candles,
        benchmark_candles=benchmark_candles,
    )

    assert not result.has("relative_strength_50")