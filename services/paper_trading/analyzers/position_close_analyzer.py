from services.paper_trading.base_paper_trading_analyzer import BasePaperTradingAnalyzer
from services.paper_trading.models import (
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)


class PositionCloseAnalyzer(BasePaperTradingAnalyzer):
    """
    Sluit een bestaande paper position deterministisch.
    """

    def analyze(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig,
        paper_trading_result: PaperTradingResult,
    ) -> PaperTradingResult:
        if not paper_trading_result.valid_operation:
            return paper_trading_result

        if paper_trading_context.normalized_operation() != "CLOSE_POSITION":
            return paper_trading_result

        trade_record = paper_trading_context.account.close_position(
            symbol=paper_trading_context.normalized_close_symbol(),
            exit_price=paper_trading_context.close_price,
            timestamp=paper_trading_context.timestamp,
            exit_reason=paper_trading_context.close_reason,
            price_precision=paper_trading_config.price_precision,
            cash_precision=paper_trading_config.cash_precision,
        )

        if trade_record is None:
            paper_trading_result.valid_operation = False
            paper_trading_result.add_warning("Paper position could not be closed; symbol is not open.")
            return paper_trading_result

        paper_trading_result.executed_trade = trade_record
        paper_trading_result.add_reason("Paper position closed.")
        return paper_trading_result
