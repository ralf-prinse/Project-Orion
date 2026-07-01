from services.performance.base_performance_analyzer import BasePerformanceAnalyzer
from services.performance.models import (
    EquityCurvePoint,
    PerformanceConfig,
    PerformanceContext,
    PerformanceResult,
)


class EquityCurveAnalyzer(BasePerformanceAnalyzer):
    """
    Berekent equity curve, total return en maximale drawdown.
    """

    def analyze(
        self,
        performance_context: PerformanceContext,
        performance_config: PerformanceConfig,
        performance_result: PerformanceResult,
    ) -> PerformanceResult:
        if not performance_result.valid_analysis:
            return performance_result

        starting_equity = performance_context.starting_equity
        if starting_equity <= 0:
            starting_equity = sum(trade.position_value() for trade in performance_context.trades)

        equity = starting_equity
        peak_equity = starting_equity
        max_drawdown_amount = 0.0
        max_drawdown_pct = 0.0
        equity_curve: list[EquityCurvePoint] = []

        for index, trade in enumerate(performance_context.trades, start=1):
            equity += trade.resolved_gross_pnl()
            peak_equity = max(peak_equity, equity)
            drawdown_amount = max(0.0, peak_equity - equity)
            drawdown_pct = (drawdown_amount / peak_equity * 100) if peak_equity > 0 else 0.0

            max_drawdown_amount = max(max_drawdown_amount, drawdown_amount)
            max_drawdown_pct = max(max_drawdown_pct, drawdown_pct)

            equity_curve.append(
                EquityCurvePoint(
                    index=index,
                    equity=round(equity, performance_config.cash_precision),
                    drawdown_amount=round(drawdown_amount, performance_config.cash_precision),
                    drawdown_pct=round(drawdown_pct, performance_config.percentage_precision),
                )
            )

        total_return_pct = (
            ((equity - starting_equity) / starting_equity) * 100
            if starting_equity > 0
            else 0.0
        )

        performance_result.starting_equity = round(starting_equity, performance_config.cash_precision)
        performance_result.ending_equity = round(equity, performance_config.cash_precision)
        performance_result.total_return_pct = round(total_return_pct, performance_config.percentage_precision)
        performance_result.max_drawdown_amount = round(max_drawdown_amount, performance_config.cash_precision)
        performance_result.max_drawdown_pct = round(max_drawdown_pct, performance_config.percentage_precision)
        performance_result.equity_curve = equity_curve
        performance_result.add_reason("Equity curve and drawdown metrics calculated.")
        return performance_result
