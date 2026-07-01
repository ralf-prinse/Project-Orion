from services.planner.base_trade_plan_analyzer import BaseTradePlanAnalyzer
from services.planner.models import (
    TradePlanContext,
    TradePlannerConfig,
    TradePlanResult,
)


class InputValidationAnalyzer(BaseTradePlanAnalyzer):
    """
    Valideert minimale invoer voor een handelsplan.

    Deze analyzer bepaalt niet of een trade aantrekkelijk is. Hij controleert
    uitsluitend of een concreet plan technisch kan worden opgebouwd.
    """

    SUPPORTED_ACTIONS = {"BUY", "SELL", "HOLD"}

    def analyze(
        self,
        trade_context: TradePlanContext,
        planner_config: TradePlannerConfig,
        trade_plan_result: TradePlanResult,
    ) -> TradePlanResult:
        action = trade_context.normalized_action()

        trade_plan_result.symbol = trade_context.symbol.upper()
        trade_plan_result.action = action if action in self.SUPPORTED_ACTIONS else "NONE"
        trade_plan_result.currency = trade_context.currency.upper()

        if action not in self.SUPPORTED_ACTIONS:
            trade_plan_result.valid_plan = False
            trade_plan_result.add_warning("Unsupported trade action; no trade plan created.")
            return trade_plan_result

        if trade_context.entry_price <= 0:
            trade_plan_result.valid_plan = False
            trade_plan_result.add_warning("Entry price must be greater than zero.")
            return trade_plan_result

        if trade_context.recommended_shares <= 0:
            trade_plan_result.valid_plan = False
            trade_plan_result.add_warning("Recommended shares must be greater than zero.")
            return trade_plan_result

        if action == "BUY" and trade_context.stop_loss <= 0:
            trade_plan_result.valid_plan = False
            trade_plan_result.add_warning("Stop-loss must be greater than zero for BUY plans.")
            return trade_plan_result

        if action == "BUY" and trade_context.stop_loss >= trade_context.entry_price:
            trade_plan_result.valid_plan = False
            trade_plan_result.add_warning("Stop-loss must be below entry price for BUY plans.")
            return trade_plan_result

        trade_plan_result.valid_plan = True
        trade_plan_result.entry_price = round(
            trade_context.entry_price,
            planner_config.price_precision,
        )
        trade_plan_result.stop_loss = round(
            trade_context.stop_loss,
            planner_config.price_precision,
        )
        trade_plan_result.shares = trade_context.recommended_shares
        trade_plan_result.add_reason("Trade plan inputs validated.")

        return trade_plan_result
