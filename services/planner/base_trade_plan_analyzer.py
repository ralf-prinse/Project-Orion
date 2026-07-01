from abc import ABC, abstractmethod

from services.planner.models import (
    TradePlanContext,
    TradePlannerConfig,
    TradePlanResult,
)


class BaseTradePlanAnalyzer(ABC):
    """
    Basisinterface voor alle Trade Planner analyzers.

    Iedere analyzer:
    - ontvangt een TradePlanContext
    - ontvangt TradePlannerConfig
    - verrijkt TradePlanResult
    - blijft deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        trade_context: TradePlanContext,
        planner_config: TradePlannerConfig,
        trade_plan_result: TradePlanResult,
    ) -> TradePlanResult:
        raise NotImplementedError
