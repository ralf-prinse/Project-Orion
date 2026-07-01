from services.planner.base_trade_plan_analyzer import BaseTradePlanAnalyzer
from services.planner.models import (
    TradePlanContext,
    TradePlannerConfig,
    TradePlanResult,
)


class RiskRewardAnalyzer(BaseTradePlanAnalyzer):
    """
    Berekent risk/reward-gegevens voor een concreet handelsplan.

    De analyzer valideert geen portefeuillerisico. Hij rekent uitsluitend het
    handelsplan door met de aangeleverde entry, stop-loss, target en shares.
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
            trade_plan_result.position_value = round(
                trade_context.entry_price * trade_context.recommended_shares,
                2,
            )
            trade_plan_result.add_reason("Non-BUY plan does not require risk/reward calculation.")
            return trade_plan_result

        risk_per_share = trade_context.entry_price - trade_context.stop_loss
        reward_per_share = trade_plan_result.target_price - trade_context.entry_price

        trade_plan_result.risk_per_share = round(risk_per_share, 4)
        trade_plan_result.total_risk_amount = round(
            trade_context.risk_amount
            if trade_context.risk_amount > 0
            else risk_per_share * trade_context.recommended_shares,
            2,
        )
        trade_plan_result.expected_reward_per_share = round(reward_per_share, 4)
        trade_plan_result.expected_reward_amount = round(
            reward_per_share * trade_context.recommended_shares,
            2,
        )
        trade_plan_result.position_value = round(
            trade_context.entry_price * trade_context.recommended_shares,
            2,
        )

        if risk_per_share <= 0:
            trade_plan_result.valid_plan = False
            trade_plan_result.add_warning("Risk per share must be greater than zero.")
            return trade_plan_result

        trade_plan_result.reward_risk_ratio = round(
            reward_per_share / risk_per_share,
            2,
        )

        if trade_plan_result.reward_risk_ratio < planner_config.minimum_reward_risk_ratio:
            trade_plan_result.add_warning("Reward/risk ratio is below configured minimum.")

        trade_plan_result.add_reason("Risk/reward metrics calculated.")
        return trade_plan_result
