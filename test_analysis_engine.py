from services.analysis.analysis_engine import AnalysisEngine


def create_dummy_candles():
    """
    Dummy historische candle data.
    In Sprint 7.1 wordt deze nog niet gebruikt,
    maar de interface blijft alvast gelijk.
    """
    return []


def main():
    engine = AnalysisEngine()

    result = engine.analyze(
        symbol="AAPL",
        candles=create_dummy_candles(),
    )

    print("=== ANALYSIS ENGINE TEST ===")
    print()

    print(f"Symbol: {result.symbol}")
    print()

    print("Scores")
    print(f"Trend: {result.trend_score}")
    print(f"Momentum: {result.momentum_score}")
    print(f"Volatility: {result.volatility_score}")
    print(f"Structure: {result.structure_score}")
    print(f"Volume: {result.volume_score}")
    print(f"Overall: {result.overall_score}")
    print()

    print("Notes")

    for note in result.notes:
        print(f"- {note}")


if __name__ == "__main__":
    main()