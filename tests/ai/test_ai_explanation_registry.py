from services.ai import AIExplanationRegistry


def test_ai_explanation_registry_has_deterministic_default_order():
    registry = AIExplanationRegistry()

    names = [definition.name for definition in registry.get_analyzers()]

    assert names == [
        "input_validation",
        "decision_explanation",
        "trade_plan_explanation",
        "performance_explanation",
        "explainability_report",
        "summary_assembler",
    ]


def test_ai_explanation_registry_returns_copy():
    registry = AIExplanationRegistry()

    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 6
