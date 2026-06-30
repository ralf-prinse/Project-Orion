from services.analysis.analyzer_registry import AnalyzerRegistry


def test_analyzer_registry_returns_default_analyzers_in_deterministic_order():
    registry = AnalyzerRegistry()

    analyzer_names = [
        analyzer_definition.name
        for analyzer_definition in registry.get_analyzers()
    ]

    assert analyzer_names == [
        "trend",
        "momentum",
        "volatility",
        "structure",
        "volume",
        "market_regime",
        "relative_strength",
        "candlestick",
    ]


def test_analyzer_registry_excludes_market_regime_from_overall_score():
    registry = AnalyzerRegistry()

    analyzer_names = [
        analyzer_definition.name
        for analyzer_definition in registry.get_overall_score_analyzers()
    ]

    assert "market_regime" not in analyzer_names

    assert analyzer_names == [
        "trend",
        "momentum",
        "volatility",
        "structure",
        "volume",
        "relative_strength",
        "candlestick",
    ]


def test_analyzer_registry_marks_only_candlestick_as_raw_candle_analyzer():
    registry = AnalyzerRegistry()

    candle_analyzers = [
        analyzer_definition.name
        for analyzer_definition in registry.get_analyzers()
        if analyzer_definition.uses_candles
    ]

    assert candle_analyzers == ["candlestick"]