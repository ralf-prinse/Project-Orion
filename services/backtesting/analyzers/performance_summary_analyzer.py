from services.backtesting.base_backtest_analyzer import BaseBacktestAnalyzer
from services.backtesting.models import BacktestConfig, BacktestContext, BacktestResult


class PerformanceSummaryAnalyzer(BaseBacktestAnalyzer):
    """
    Berekent compacte performance-statistieken voor de backtest.
    """

    def analyze(
        self,
        backtest_context: BacktestContext,
        backtest_config: BacktestConfig,
        backtest_result: BacktestResult,
    ) -> BacktestResult:
        if not backtest_result.valid_backtest:
            backtest_result.add_reason("No valid backtest performance summary assembled.")
            return backtest_result

        trades = backtest_result.trades
        backtest_result.total_trades = len(trades)
        backtest_result.winning_trades = sum(1 for trade in trades if trade.gross_pnl > 0)
        backtest_result.losing_trades = sum(1 for trade in trades if trade.gross_pnl < 0)
        backtest_result.total_gross_pnl = round(
            sum(trade.gross_pnl for trade in trades),
            2,
        )

        if backtest_result.total_trades > 0:
            backtest_result.win_rate = round(
                backtest_result.winning_trades / backtest_result.total_trades * 100,
                backtest_config.percentage_precision,
            )

        if backtest_context.initial_capital > 0:
            backtest_result.total_return_pct = round(
                backtest_result.total_gross_pnl / backtest_context.initial_capital * 100,
                backtest_config.percentage_precision,
            )

        backtest_result.max_drawdown = self._calculate_max_drawdown(
            trades=trades,
            initial_capital=backtest_context.initial_capital,
            percentage_precision=backtest_config.percentage_precision,
        )
        backtest_result.add_reason("Backtest performance summary calculated.")
        return backtest_result

    def _calculate_max_drawdown(
        self,
        trades,
        initial_capital: float,
        percentage_precision: int,
    ) -> float:
        if initial_capital <= 0:
            return 0.0

        equity = initial_capital
        peak = initial_capital
        max_drawdown = 0.0

        for trade in trades:
            equity += trade.gross_pnl
            peak = max(peak, equity)
            drawdown = (peak - equity) / peak * 100 if peak > 0 else 0.0
            max_drawdown = max(max_drawdown, drawdown)

        return round(max_drawdown, percentage_precision)
