from services.signals.signal_registry import SignalRegistry


def test_signal_registry_returns_default_analyzers_in_deterministic_order():
    registry = SignalRegistry()

    analyzer_names = [
        analyzer_definition.name
        for analyzer_definition in registry.get_analyzers()
    ]

    assert analyzer_names == [
        "entry",
    ]


def test_signal_registry_returns_copy_of_registered_analyzers():
    registry = SignalRegistry()

    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 1