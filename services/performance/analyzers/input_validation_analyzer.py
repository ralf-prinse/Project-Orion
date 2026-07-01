from services.performance.base_performance_analyzer import BasePerformanceAnalyzer
from services.performance.models import (
    PerformanceConfig,
    PerformanceContext,
    PerformanceResult,
)


class InputValidationAnalyzer(BasePerformanceAnalyzer):
    """
    Valideert of Performance Analytics veilig kan worden uitgevoerd.
    """

    def analyze(
        self,
        performance_context: PerformanceContext,
        performance_config: PerformanceConfig,
        performance_result: PerformanceResult,
    ) -> PerformanceResult:
        if performance_context.starting_equity < 0:
            performance_result.valid_analysis = False
            performance_result.add_warning("Starting equity must be zero or greater.")
            return performance_result

        if not performance_context.trades:
            performance_result.valid_analysis = False
            performance_result.starting_equity = round(
                performance_context.starting_equity,
                performance_config.cash_precision,
            )
            performance_result.ending_equity = performance_result.starting_equity
            performance_result.add_warning("At least one trade is required for performance analytics.")
            return performance_result

        invalid_trades = [
            trade
            for trade in performance_context.trades
            if trade.entry_price <= 0 or trade.exit_price <= 0 or trade.quantity <= 0
        ]

        if invalid_trades:
            performance_result.valid_analysis = False
            performance_result.add_warning("All trades require positive prices and positive quantity.")
            return performance_result

        performance_result.valid_analysis = True
        performance_result.starting_equity = round(
            performance_context.starting_equity,
            performance_config.cash_precision,
        )
        performance_result.add_reason("Performance analytics input validation passed.")
        return performance_result
