from services.paper_trading.paper_trading_registry import PaperTradingRegistry


def test_paper_trading_registry_returns_default_analyzers_in_order():
    registry = PaperTradingRegistry()

    names = [definition.name for definition in registry.get_analyzers()]

    assert names == [
        "input_validation",
        "trade_execution",
        "mark_to_market",
        "position_close",
        "account_summary",
    ]


def test_paper_trading_registry_returns_copy():
    registry = PaperTradingRegistry()

    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 5
