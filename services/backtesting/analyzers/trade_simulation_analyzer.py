from services.backtesting.base_backtest_analyzer import BaseBacktestAnalyzer
from services.backtesting.models import BacktestConfig, BacktestContext, BacktestResult
from services.backtesting.trade_simulator import TradeSimulator


class TradeSimulationAnalyzer(BaseBacktestAnalyzer):
    """
    Simuleert één bestaand TradePlanResult over historische candles.
    """

    def __init__(self, trade_simulator: TradeSimulator | None = None):
        self.trade_simulator = trade_simulator or TradeSimulator()

    def analyze(
        self,
        backtest_context: BacktestContext,
        backtest_config: BacktestConfig,
        backtest_result: BacktestResult,
    ) -> BacktestResult:
        if not backtest_result.valid_backtest:
            return backtest_result

        trade = self.trade_simulator.simulate(
            symbol=backtest_result.symbol,
            trade_plan=backtest_context.trade_plan,
            candles=backtest_context.candles,
            config=backtest_config,
        )

        if trade is None:
            backtest_result.valid_backtest = False
            backtest_result.add_warning("Entry price was not reached during the backtest period.")
            return backtest_result

        backtest_result.add_trade(trade)
        backtest_result.add_reason("Trade plan simulated over historical candles.")
        return backtest_result
