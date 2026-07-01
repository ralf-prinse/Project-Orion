from services.planner.trade_plan_registry import TradePlanRegistry


def test_trade_plan_registry_default_order_is_deterministic():
    registry = TradePlanRegistry()

    names = [definition.name for definition in registry.get_analyzers()]

    assert names == [
        "input_validation",
        "target_price",
        "risk_reward",
        "trade_plan_summary",
    ]


def test_trade_plan_registry_returns_copy():
    registry = TradePlanRegistry()

    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 4
