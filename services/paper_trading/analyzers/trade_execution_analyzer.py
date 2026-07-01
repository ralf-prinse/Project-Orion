from services.paper_trading.base_paper_trading_analyzer import BasePaperTradingAnalyzer
from services.paper_trading.models import (
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)


class TradeExecutionAnalyzer(BasePaperTradingAnalyzer):
    """
    Opent een paper position op basis van een bestaand TradePlanResult.
    """

    def analyze(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig,
        paper_trading_result: PaperTradingResult,
    ) -> PaperTradingResult:
        if not paper_trading_result.valid_operation:
            return paper_trading_result

        if paper_trading_context.normalized_operation() != "EXECUTE_TRADE_PLAN":
            return paper_trading_result

        trade_plan = paper_trading_context.trade_plan
        account = paper_trading_context.account
        symbol = trade_plan.symbol.upper()
        required_cash = round(trade_plan.shares * trade_plan.entry_price, paper_trading_config.cash_precision)

        if account.has_position(symbol) and not paper_trading_config.allow_position_replacement:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Paper trade blocked; position already exists.")
            return paper_trading_result

        if (account.cash_balance or 0.0) < required_cash:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Paper trade blocked; insufficient cash balance.")
            return paper_trading_result

        if account.has_position(symbol) and paper_trading_config.allow_position_replacement:
            account.close_position(
                symbol=symbol,
                exit_price=trade_plan.entry_price,
                timestamp=paper_trading_context.timestamp,
                exit_reason="REPLACED",
                price_precision=paper_trading_config.price_precision,
                cash_precision=paper_trading_config.cash_precision,
            )

        paper_trading_result.executed_trade = account.open_position(
            trade_plan=trade_plan,
            timestamp=paper_trading_context.timestamp,
            price_precision=paper_trading_config.price_precision,
            cash_precision=paper_trading_config.cash_precision,
        )
        paper_trading_result.add_reason("Paper trade executed from deterministic trade plan.")
        return paper_trading_result
