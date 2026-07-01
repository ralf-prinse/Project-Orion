from abc import ABC, abstractmethod

from services.performance.models import (
    PerformanceConfig,
    PerformanceContext,
    PerformanceResult,
)


class BasePerformanceAnalyzer(ABC):
    """
    Basisinterface voor alle Performance Analytics analyzers.

    Iedere analyzer:
    - ontvangt PerformanceContext
    - ontvangt PerformanceConfig
    - verrijkt PerformanceResult
    - blijft volledig deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        performance_context: PerformanceContext,
        performance_config: PerformanceConfig,
        performance_result: PerformanceResult,
    ) -> PerformanceResult:
        raise NotImplementedError
