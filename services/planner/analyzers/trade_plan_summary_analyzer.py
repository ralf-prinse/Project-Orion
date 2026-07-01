from services.planner.base_trade_plan_analyzer import BaseTradePlanAnalyzer
from services.planner.models import (
    TradePlanContext,
    TradePlannerConfig,
    TradePlanResult,
)


class TradePlanSummaryAnalyzer(BaseTradePlanAnalyzer):
    """
    Rondt het TradePlanResult af met een compacte deterministische samenvatting.
    """

    def analyze(
        self,
        trade_context: TradePlanContext,
        planner_config: TradePlannerConfig,
        trade_plan_result: TradePlanResult,
    ) -> TradePlanResult:
        if not trade_plan_result.valid_plan:
            trade_plan_result.add_reason("No executable trade plan assembled.")
            return trade_plan_result

        if trade_plan_result.action == "BUY":
            trade_plan_result.add_reason("Executable BUY trade plan assembled.")
            return trade_plan_result

        trade_plan_result.add_reason(f"Executable {trade_plan_result.action} trade plan assembled.")
        return trade_plan_result
