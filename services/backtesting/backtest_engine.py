from core.orchestration.analyzer_runner import AnalyzerRunner
from services.backtesting.backtest_registry import BacktestRegistry
from services.backtesting.models import BacktestConfig, BacktestContext, BacktestResult


class BacktestEngine:
    """
    Centrale Backtesting Engine van Project Orion.

    De engine simuleert bestaande, deterministische handelsplannen over
    historische candles.

    De engine:
    - bevat zelf geen backtestlogica
    - gebruikt BacktestRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - retourneert een deterministisch BacktestResult
    """

    def __init__(
        self,
        backtest_registry: BacktestRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.backtest_registry = backtest_registry or BacktestRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def run(
        self,
        backtest_context: BacktestContext,
        backtest_config: BacktestConfig | None = None,
    ) -> BacktestResult:
        config = backtest_config or BacktestConfig()
        backtest_result = BacktestResult(
            symbol=backtest_context.resolved_symbol(),
        )

        return self.analyzer_runner.run(
            registry=self.backtest_registry,
            result=backtest_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    backtest_context=backtest_context,
                    backtest_config=config,
                    backtest_result=result,
                )
            ),
        )
