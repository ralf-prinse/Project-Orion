from services.risk import RiskRegistry


def test_risk_registry_returns_default_analyzers_in_deterministic_order():
    registry = RiskRegistry()

    analyzer_names = [definition.name for definition in registry.get_analyzers()]

    assert analyzer_names == [
        "risk_summary",
        "trade_risk",
        "portfolio_risk",
        "drawdown",
        "capital_protection",
        "position_exposure_risk",
    ]


def test_risk_registry_returns_copy_of_analyzers():
    registry = RiskRegistry()

    first = registry.get_analyzers()
    second = registry.get_analyzers()

    assert first is not second
    assert [definition.name for definition in first] == [
        definition.name for definition in second
    ]
