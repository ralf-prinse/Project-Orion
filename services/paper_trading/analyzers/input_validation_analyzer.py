from services.paper_trading.base_paper_trading_analyzer import BasePaperTradingAnalyzer
from services.paper_trading.models import (
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)


class InputValidationAnalyzer(BasePaperTradingAnalyzer):
    """
    Valideert minimale invoer voor paper-trading operaties.
    """

    SUPPORTED_OPERATIONS = {"EXECUTE_TRADE_PLAN", "MARK_TO_MARKET", "CLOSE_POSITION"}

    def analyze(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig,
        paper_trading_result: PaperTradingResult,
    ) -> PaperTradingResult:
        operation = paper_trading_context.normalized_operation()
        paper_trading_result.operation = operation
        paper_trading_result.account = paper_trading_context.account

        if operation not in self.SUPPORTED_OPERATIONS:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Unsupported paper-trading operation.")
            return paper_trading_result

        if paper_trading_context.account.starting_cash < 0:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Starting cash cannot be negative.")
            return paper_trading_result

        if operation == "EXECUTE_TRADE_PLAN":
            self._validate_trade_plan(paper_trading_context, paper_trading_result)

        if operation == "CLOSE_POSITION":
            self._validate_close_position(paper_trading_context, paper_trading_result)

        if paper_trading_result.valid_operation:
            paper_trading_result.add_reason("Paper-trading inputs validated.")

        return paper_trading_result

    def _validate_trade_plan(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_result: PaperTradingResult,
    ):
        trade_plan = paper_trading_context.trade_plan

        if trade_plan is None:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("A trade plan is required to execute a paper trade.")
            return

        if not trade_plan.valid_plan:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Trade plan is not valid; paper trade skipped.")
            return

        if trade_plan.action != "BUY":
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Only BUY trade plans can open paper positions.")
            return

        if trade_plan.shares <= 0:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Trade plan must contain a positive share quantity.")
            return

        if trade_plan.entry_price <= 0:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Trade plan must contain a positive entry price.")
            return

    def _validate_close_position(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_result: PaperTradingResult,
    ):
        if not paper_trading_context.normalized_close_symbol():
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("A symbol is required to close a paper position.")
            return

        if paper_trading_context.close_price <= 0:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Close price must be greater than zero.")
