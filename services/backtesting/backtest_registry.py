from dataclasses import dataclass
from typing import Any

from services.backtesting.analyzers.input_validation_analyzer import InputValidationAnalyzer
from services.backtesting.analyzers.performance_summary_analyzer import PerformanceSummaryAnalyzer
from services.backtesting.analyzers.trade_simulation_analyzer import TradeSimulationAnalyzer


@dataclass(frozen=True)
class BacktestAnalyzerDefinition:
    """
    Registratiegegevens voor één Backtesting analyzer.
    """

    name: str
    analyzer: Any


class BacktestRegistry:
    """
    Centrale registry voor Backtesting analyzers.

    De registry bepaalt de deterministische uitvoervolgorde en bevat zelf geen
    simulatie-, performance- of tradinglogica.
    """

    def __init__(
        self,
        analyzers: list[BacktestAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[BacktestAnalyzerDefinition]:
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[BacktestAnalyzerDefinition]:
        return [
            BacktestAnalyzerDefinition(
                name="input_validation",
                analyzer=InputValidationAnalyzer(),
            ),
            BacktestAnalyzerDefinition(
                name="trade_simulation",
                analyzer=TradeSimulationAnalyzer(),
            ),
            BacktestAnalyzerDefinition(
                name="performance_summary",
                analyzer=PerformanceSummaryAnalyzer(),
            ),
        ]
