import pandas as pd

from services.analysis.analysis_engine import AnalysisEngine


def build_test_candles() -> pd.DataFrame:
    rows = []

    for index in range(100):
        close = 100 + index

        rows.append(
            {
                "Open": close - 1,
                "High": close + 2,
                "Low": close - 2,
                "Close": close,
                "Volume": 1_000_000,
            }
        )

    return pd.DataFrame(rows)


def main():
    print("=== ANALYSIS ENGINE TEST ===")
    print()

    candles = build_test_candles()
    engine = AnalysisEngine()

    result = engine.analyze(
        symbol="TEST",
        candles=candles,
    )

    indicators = engine.indicator_engine.calculate(
        symbol="TEST",
        candles=candles,
    )

    print(f"Symbol: {result.symbol}")
    print()

    print("Basic Indicators")
    print(f"SMA20: {indicators.get('sma20')}")
    print(f"SMA50: {indicators.get('sma50')}")
    print(f"EMA20: {indicators.get('ema20')}")
    print(f"EMA50: {indicators.get('ema50')}")
    print(f"RSI14: {indicators.get('rsi14')}")
    print()

    print("Advanced Indicators")
    print(f"MACD: {indicators.get('macd')}")
    print(f"ATR14: {indicators.get('atr14')}")
    print(f"Bollinger Bands: {indicators.get('bollinger')}")
    print(f"ADX14: {indicators.get('adx14')}")
    print()

    print("Analysis Scores")
    print(f"Trend Score: {result.trend_score}")
    print(f"Momentum Score: {result.momentum_score}")
    print(f"Volatility Score: {result.volatility_score}")
    print(f"Overall Score: {result.overall_score}")
    print()

    print("Analysis Notes")
    for note in result.notes:
        print(f"- {note}")

    assert result.symbol == "TEST"
    assert result.overall_score > 0
    assert indicators.get("sma20") is not None
    assert indicators.get("sma50") is not None
    assert indicators.get("ema20") is not None
    assert indicators.get("ema50") is not None
    assert indicators.get("rsi14") is not None

    print()
    print("Analysis Engine test succesvol afgerond.")


if __name__ == "__main__":
    main()