from services.paper_trading.base_paper_trading_analyzer import BasePaperTradingAnalyzer
from services.paper_trading.models import (
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)


class MarkToMarketAnalyzer(BasePaperTradingAnalyzer):
    """
    Werkt open paper positions bij met aangeleverde marktprijzen.
    """

    def analyze(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig,
        paper_trading_result: PaperTradingResult,
    ) -> PaperTradingResult:
        if not paper_trading_result.valid_operation:
            return paper_trading_result

        if paper_trading_context.normalized_operation() != "MARK_TO_MARKET":
            return paper_trading_result

        updated = 0
        for symbol, market_price in paper_trading_context.market_prices.items():
            if market_price <= 0:
                paper_trading_result.add_warning(
                    f"Market price for {symbol.upper()} ignored; price must be greater than zero."
                )
                continue

            if paper_trading_context.account.has_position(symbol):
                paper_trading_context.account.update_market_price(
                    symbol=symbol,
                    market_price=market_price,
                    price_precision=paper_trading_config.price_precision,
                )
                updated += 1

        paper_trading_result.add_reason(f"Mark-to-market updated {updated} open position(s).")
        return paper_trading_result
