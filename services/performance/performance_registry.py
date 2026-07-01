from dataclasses import dataclass
from typing import Any

from services.performance.analyzers.equity_curve_analyzer import EquityCurveAnalyzer
from services.performance.analyzers.input_validation_analyzer import InputValidationAnalyzer
from services.performance.analyzers.trade_metrics_analyzer import TradeMetricsAnalyzer


@dataclass(frozen=True)
class PerformanceAnalyzerDefinition:
    """
    Registratiegegevens voor één Performance Analytics analyzer.
    """

    name: str
    analyzer: Any


class PerformanceRegistry:
    """
    Centrale registry voor Performance Analytics analyzers.

    De registry bepaalt de deterministische uitvoervolgorde en bevat zelf geen
    statistiek-, trading-, portfolio- of risklogica.
    """

    def __init__(
        self,
        analyzers: list[PerformanceAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[PerformanceAnalyzerDefinition]:
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[PerformanceAnalyzerDefinition]:
        return [
            PerformanceAnalyzerDefinition(
                name="input_validation",
                analyzer=InputValidationAnalyzer(),
            ),
            PerformanceAnalyzerDefinition(
                name="trade_metrics",
                analyzer=TradeMetricsAnalyzer(),
            ),
            PerformanceAnalyzerDefinition(
                name="equity_curve",
                analyzer=EquityCurveAnalyzer(),
            ),
        ]
