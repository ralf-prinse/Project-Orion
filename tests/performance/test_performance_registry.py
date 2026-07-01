from services.performance.analyzers.equity_curve_analyzer import EquityCurveAnalyzer
from services.performance.analyzers.input_validation_analyzer import InputValidationAnalyzer
from services.performance.analyzers.trade_metrics_analyzer import TradeMetricsAnalyzer
from services.performance.performance_registry import PerformanceRegistry


def test_performance_registry_returns_default_analyzers_in_deterministic_order():
    registry = PerformanceRegistry()
    analyzers = registry.get_analyzers()

    assert [definition.name for definition in analyzers] == [
        "input_validation",
        "trade_metrics",
        "equity_curve",
    ]
    assert isinstance(analyzers[0].analyzer, InputValidationAnalyzer)
    assert isinstance(analyzers[1].analyzer, TradeMetricsAnalyzer)
    assert isinstance(analyzers[2].analyzer, EquityCurveAnalyzer)


def test_performance_registry_returns_copy_of_analyzers():
    registry = PerformanceRegistry()
    analyzers = registry.get_analyzers()
    analyzers.clear()

    assert len(registry.get_analyzers()) == 3
