from core.orchestration.analyzer_runner import AnalyzerRunner
from services.backtesting.models import BacktestResult
from services.paper_trading.models import PaperAccount
from services.performance.models import (
    PerformanceConfig,
    PerformanceContext,
    PerformanceResult,
    PerformanceTrade,
)
from services.performance.performance_registry import PerformanceRegistry


class PerformanceEngine:
    """
    Centrale Performance Analytics Engine van Project Orion.

    De engine berekent professionele statistieken over bestaande trade-resultaten.

    De engine:
    - bevat zelf geen statistieklogica
    - gebruikt PerformanceRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - neemt geen investerings-, portfolio- of riskbeslissingen
    """

    def __init__(
        self,
        performance_registry: PerformanceRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.performance_registry = performance_registry or PerformanceRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def run(
        self,
        performance_context: PerformanceContext,
        performance_config: PerformanceConfig | None = None,
    ) -> PerformanceResult:
        config = performance_config or PerformanceConfig()
        performance_result = PerformanceResult(
            label=performance_context.label,
        )

        return self.analyzer_runner.run(
            registry=self.performance_registry,
            result=performance_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    performance_context=performance_context,
                    performance_config=config,
                    performance_result=result,
                )
            ),
        )

    def analyze_backtest_result(
        self,
        backtest_result: BacktestResult,
        starting_equity: float = 0.0,
        performance_config: PerformanceConfig | None = None,
    ) -> PerformanceResult:
        trades = [
            PerformanceTrade(
                symbol=trade.symbol,
                entry_price=trade.entry_price,
                exit_price=trade.exit_price,
                quantity=trade.shares,
                entry_date=trade.entry_date,
                exit_date=trade.exit_date,
                gross_pnl=trade.gross_pnl,
            )
            for trade in backtest_result.trades
        ]

        context = PerformanceContext(
            trades=trades,
            starting_equity=starting_equity,
            label=f"Backtest {backtest_result.symbol}".strip(),
        )
        return self.run(context, performance_config)

    def analyze_paper_account(
        self,
        paper_account: PaperAccount,
        performance_config: PerformanceConfig | None = None,
    ) -> PerformanceResult:
        trades = [
            PerformanceTrade(
                symbol=trade.symbol,
                entry_price=trade.entry_price,
                exit_price=trade.exit_price,
                quantity=trade.quantity,
                entry_date=trade.entry_date,
                exit_date=trade.exit_date,
                gross_pnl=trade.gross_pnl,
                currency=trade.currency,
            )
            for trade in paper_account.trade_history
            if trade.status == "CLOSED"
        ]

        context = PerformanceContext(
            trades=trades,
            starting_equity=paper_account.starting_cash,
            label="Paper Trading",
        )
        return self.run(context, performance_config)
