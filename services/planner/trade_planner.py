from core.orchestration.analyzer_runner import AnalyzerRunner
from services.planner.models import (
    TradePlanContext,
    TradePlannerConfig,
    TradePlanResult,
)
from services.planner.trade_plan_registry import TradePlanRegistry


class TradePlanner:
    """
    Centrale Trade Planner van Project Orion.

    De Trade Planner zet goedgekeurde deterministische inputs om naar een
    concreet handelsplan.

    De planner:
    - bevat zelf geen trade-planninglogica
    - gebruikt TradePlanRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - retourneert een deterministisch TradePlanResult
    """

    def __init__(
        self,
        trade_plan_registry: TradePlanRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.trade_plan_registry = trade_plan_registry or TradePlanRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def create_plan(
        self,
        trade_context: TradePlanContext,
        planner_config: TradePlannerConfig | None = None,
    ) -> TradePlanResult:
        config = planner_config or TradePlannerConfig()

        trade_plan_result = TradePlanResult(
            symbol=trade_context.symbol.upper(),
            currency=trade_context.currency.upper(),
        )

        return self.analyzer_runner.run(
            registry=self.trade_plan_registry,
            result=trade_plan_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    trade_context=trade_context,
                    planner_config=config,
                    trade_plan_result=result,
                )
            ),
        )
