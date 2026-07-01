from services.performance.base_performance_analyzer import BasePerformanceAnalyzer
from services.performance.models import (
    PerformanceConfig,
    PerformanceContext,
    PerformanceResult,
)


class TradeMetricsAnalyzer(BasePerformanceAnalyzer):
    """
    Berekent deterministische trade-statistieken.
    """

    def analyze(
        self,
        performance_context: PerformanceContext,
        performance_config: PerformanceConfig,
        performance_result: PerformanceResult,
    ) -> PerformanceResult:
        if not performance_result.valid_analysis:
            return performance_result

        trades = performance_context.trades
        pnl_values = [trade.resolved_gross_pnl() for trade in trades]
        winning_values = [pnl for pnl in pnl_values if pnl > 0]
        losing_values = [pnl for pnl in pnl_values if pnl < 0]
        breakeven_values = [pnl for pnl in pnl_values if pnl == 0]

        total_trades = len(trades)
        winning_trades = len(winning_values)
        losing_trades = len(losing_values)
        breakeven_trades = len(breakeven_values)

        gross_profit = sum(winning_values)
        gross_loss = sum(losing_values)
        net_pnl = sum(pnl_values)

        average_win = gross_profit / winning_trades if winning_trades else 0.0
        average_loss = gross_loss / losing_trades if losing_trades else 0.0
        average_trade = net_pnl / total_trades if total_trades else 0.0

        win_rate_decimal = winning_trades / total_trades if total_trades else 0.0
        loss_rate_decimal = losing_trades / total_trades if total_trades else 0.0
        expectancy = (
            (win_rate_decimal * average_win)
            + (loss_rate_decimal * average_loss)
        )
        profit_factor = gross_profit / abs(gross_loss) if gross_loss < 0 else 0.0
        payoff_ratio = average_win / abs(average_loss) if average_loss < 0 else 0.0

        performance_result.total_trades = total_trades
        performance_result.winning_trades = winning_trades
        performance_result.losing_trades = losing_trades
        performance_result.breakeven_trades = breakeven_trades
        performance_result.win_rate = round(win_rate_decimal * 100, performance_config.percentage_precision)
        performance_result.loss_rate = round(loss_rate_decimal * 100, performance_config.percentage_precision)
        performance_result.gross_profit = round(gross_profit, performance_config.cash_precision)
        performance_result.gross_loss = round(gross_loss, performance_config.cash_precision)
        performance_result.net_pnl = round(net_pnl, performance_config.cash_precision)
        performance_result.average_win = round(average_win, performance_config.cash_precision)
        performance_result.average_loss = round(average_loss, performance_config.cash_precision)
        performance_result.average_trade = round(average_trade, performance_config.cash_precision)
        performance_result.expectancy = round(expectancy, performance_config.cash_precision)
        performance_result.profit_factor = round(profit_factor, performance_config.ratio_precision)
        performance_result.payoff_ratio = round(payoff_ratio, performance_config.ratio_precision)
        performance_result.add_reason("Trade performance metrics calculated.")
        return performance_result
