from services.market_data.yahoo_historical_provider import YahooHistoricalDataProvider
from services.analysis.analysis_engine import AnalysisEngine


def main():
    print("=== ANALYSIS ENGINE TEST ===")
    print()

    provider = YahooHistoricalDataProvider()
    history = provider.get_history(
        symbols=["AAPL"],
        period="6mo",
        interval="1d",
    )

    candles = history.get("AAPL")

    if candles is None or candles.empty:
        print("Geen candles ontvangen voor AAPL")
        return

    engine = AnalysisEngine()

    result = engine.analyze(
        symbol="AAPL",
        candles=candles,
    )

    indicators = engine.indicator_engine.calculate(
        symbol="AAPL",
        candles=candles,
    )

    print(f"Symbol: {result.symbol}")
    print()

    print("Indicatoren")
    print(f"SMA20: {indicators.get('sma20')}")
    print(f"SMA50: {indicators.get('sma50')}")
    print(f"EMA20: {indicators.get('ema20')}")
    print(f"EMA50: {indicators.get('ema50')}")
    print(f"RSI14: {indicators.get('rsi14')}")
    print()

    print("Analysis Notes")
    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    main()