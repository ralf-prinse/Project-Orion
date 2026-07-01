from abc import ABC, abstractmethod

from services.backtesting.models import BacktestConfig, BacktestContext, BacktestResult


class BaseBacktestAnalyzer(ABC):
    """
    Basisinterface voor alle Backtesting analyzers.

    Iedere analyzer:
    - ontvangt BacktestContext
    - ontvangt BacktestConfig
    - verrijkt BacktestResult
    - blijft volledig deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        backtest_context: BacktestContext,
        backtest_config: BacktestConfig,
        backtest_result: BacktestResult,
    ) -> BacktestResult:
        raise NotImplementedError
