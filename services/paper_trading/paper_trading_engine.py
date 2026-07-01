from core.orchestration.analyzer_runner import AnalyzerRunner
from services.paper_trading.models import (
    PaperAccount,
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)
from services.paper_trading.paper_trading_registry import PaperTradingRegistry
from services.planner.models import TradePlanResult


class PaperTradingEngine:
    """
    Centrale Paper Trading Engine van Project Orion.

    De engine simuleert bestaande TradePlanResult-objecten op een paper account.

    De engine:
    - bevat zelf geen trade-executie-, mark-to-market- of sluitlogica
    - gebruikt PaperTradingRegistry voor analyzer-volgorde
    - gebruikt AnalyzerRunner voor generieke orchestratie
    - retourneert een deterministisch PaperTradingResult
    """

    def __init__(
        self,
        paper_trading_registry: PaperTradingRegistry | None = None,
        analyzer_runner: AnalyzerRunner | None = None,
    ):
        self.paper_trading_registry = paper_trading_registry or PaperTradingRegistry()
        self.analyzer_runner = analyzer_runner or AnalyzerRunner()

    def run(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig | None = None,
    ) -> PaperTradingResult:
        config = paper_trading_config or PaperTradingConfig()
        paper_trading_result = PaperTradingResult(
            operation=paper_trading_context.normalized_operation(),
            account=paper_trading_context.account,
        )

        return self.analyzer_runner.run(
            registry=self.paper_trading_registry,
            result=paper_trading_result,
            analyzer_executor=lambda analyzer_definition, result: (
                analyzer_definition.analyzer.analyze(
                    paper_trading_context=paper_trading_context,
                    paper_trading_config=config,
                    paper_trading_result=result,
                )
            ),
        )

    def execute_trade_plan(
        self,
        account: PaperAccount,
        trade_plan: TradePlanResult,
        timestamp: str = "",
        paper_trading_config: PaperTradingConfig | None = None,
    ) -> PaperTradingResult:
        return self.run(
            paper_trading_context=PaperTradingContext(
                account=account,
                operation="EXECUTE_TRADE_PLAN",
                trade_plan=trade_plan,
                timestamp=timestamp,
            ),
            paper_trading_config=paper_trading_config,
        )

    def mark_to_market(
        self,
        account: PaperAccount,
        market_prices: dict[str, float],
        paper_trading_config: PaperTradingConfig | None = None,
    ) -> PaperTradingResult:
        return self.run(
            paper_trading_context=PaperTradingContext(
                account=account,
                operation="MARK_TO_MARKET",
                market_prices=market_prices,
            ),
            paper_trading_config=paper_trading_config,
        )

    def close_position(
        self,
        account: PaperAccount,
        symbol: str,
        close_price: float,
        timestamp: str = "",
        close_reason: str = "MANUAL",
        paper_trading_config: PaperTradingConfig | None = None,
    ) -> PaperTradingResult:
        return self.run(
            paper_trading_context=PaperTradingContext(
                account=account,
                operation="CLOSE_POSITION",
                close_symbol=symbol,
                close_price=close_price,
                close_reason=close_reason,
                timestamp=timestamp,
            ),
            paper_trading_config=paper_trading_config,
        )
