from services.planner.base_trade_plan_analyzer import BaseTradePlanAnalyzer
from services.planner.models import (
    TradePlanContext,
    TradePlannerConfig,
    TradePlanResult,
)


class TargetPriceAnalyzer(BaseTradePlanAnalyzer):
    """
    Bepaalt een deterministische target price voor het handelsplan.

    Als de context al een target_price bevat, wordt deze gebruikt. Anders wordt
    een doelprijs berekend op basis van de ingestelde reward/risk-ratio.
    """

    def analyze(
        self,
        trade_context: TradePlanContext,
        planner_config: TradePlannerConfig,
        trade_plan_result: TradePlanResult,
    ) -> TradePlanResult:
        if not trade_plan_result.valid_plan:
            return trade_plan_result

        if trade_plan_result.action != "BUY":
            trade_plan_result.target_price = 0.0
            return trade_plan_result

        risk_per_share = trade_context.entry_price - trade_context.stop_loss

        if trade_context.target_price is not None:
            target_price = trade_context.target_price
            trade_plan_result.add_reason("Target price supplied by context.")
        else:
            target_price = trade_context.entry_price + (
                risk_per_share * planner_config.default_reward_risk_ratio
            )
            trade_plan_result.add_reason("Target price calculated from default reward/risk ratio.")

        trade_plan_result.target_price = round(
            target_price,
            planner_config.price_precision,
        )

        return trade_plan_result
