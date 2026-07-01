from services.paper_trading.base_paper_trading_analyzer import BasePaperTradingAnalyzer
from services.paper_trading.models import (
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)


class AccountSummaryAnalyzer(BasePaperTradingAnalyzer):
    """
    Berekent deterministische account-samenvatting na een paper-trading operatie.
    """

    def analyze(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig,
        paper_trading_result: PaperTradingResult,
    ) -> PaperTradingResult:
        account = paper_trading_context.account
        paper_trading_result.account = account
        paper_trading_result.cash_balance = round(account.cash_balance or 0.0, paper_trading_config.cash_precision)
        paper_trading_result.equity = round(account.equity(), paper_trading_config.cash_precision)
        paper_trading_result.open_positions = account.open_position_count()
        paper_trading_result.realized_pnl = round(account.realized_pnl(), paper_trading_config.cash_precision)
        paper_trading_result.unrealized_pnl = round(account.unrealized_pnl(), paper_trading_config.cash_precision)
        paper_trading_result.add_reason("Paper-trading account summary calculated.")
        return paper_trading_result
