from services.backtesting.backtest_registry import BacktestRegistry


def test_backtest_registry_returns_default_analyzers_in_order():
    registry = BacktestRegistry()

    analyzer_names = [definition.name for definition in registry.get_analyzers()]

    assert analyzer_names == [
        "input_validation",
        "trade_simulation",
        "performance_summary",
    ]


def test_backtest_registry_returns_copy_of_analyzers():
    registry = BacktestRegistry()

    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 3
