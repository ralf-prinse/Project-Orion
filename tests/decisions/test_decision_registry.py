from services.decisions.registry import DecisionRegistry


def test_decision_registry_returns_default_analyzers_in_deterministic_order():
    registry = DecisionRegistry()

    analyzer_names = [
        analyzer_definition.name
        for analyzer_definition in registry.get_analyzers()
    ]

    assert analyzer_names == [
        "signal_validation",
        "portfolio_validation",
        "risk_validation",
        "decision_assembler",
    ]


def test_decision_registry_returns_copy_of_registered_analyzers():
    registry = DecisionRegistry()

    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 4