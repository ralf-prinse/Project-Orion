from services.backtesting.base_backtest_analyzer import BaseBacktestAnalyzer
from services.backtesting.models import BacktestConfig, BacktestContext, BacktestResult


class InputValidationAnalyzer(BaseBacktestAnalyzer):
    """
    Valideert minimale invoer voor een backtest.

    Deze analyzer beoordeelt niet of een strategie goed is. Hij controleert
    uitsluitend of een bestaand handelsplan gesimuleerd kan worden.
    """

    def analyze(
        self,
        backtest_context: BacktestContext,
        backtest_config: BacktestConfig,
        backtest_result: BacktestResult,
    ) -> BacktestResult:
        trade_plan = backtest_context.trade_plan
        backtest_result.symbol = backtest_context.resolved_symbol()

        if not trade_plan.valid_plan:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Trade plan is not valid; backtest skipped.")
            return backtest_result

        if trade_plan.action != "BUY":
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Only BUY trade plans are supported by the backtesting foundation.")
            return backtest_result

        if trade_plan.entry_price <= 0:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Entry price must be greater than zero.")
            return backtest_result

        if trade_plan.stop_loss <= 0:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Stop-loss must be greater than zero.")
            return backtest_result

        if trade_plan.target_price <= 0:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Target price must be greater than zero.")
            return backtest_result

        if trade_plan.shares <= 0:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Share quantity must be greater than zero.")
            return backtest_result

        if len(backtest_context.candles) == 0:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("At least one candle is required for backtesting.")
            return backtest_result

        backtest_result.valid_backtest = True
        backtest_result.add_reason("Backtest inputs validated.")
        return backtest_result
