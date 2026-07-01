from dataclasses import dataclass
from typing import Any

from services.paper_trading.analyzers.account_summary_analyzer import AccountSummaryAnalyzer
from services.paper_trading.analyzers.input_validation_analyzer import InputValidationAnalyzer
from services.paper_trading.analyzers.mark_to_market_analyzer import MarkToMarketAnalyzer
from services.paper_trading.analyzers.position_close_analyzer import PositionCloseAnalyzer
from services.paper_trading.analyzers.trade_execution_analyzer import TradeExecutionAnalyzer


@dataclass(frozen=True)
class PaperTradingAnalyzerDefinition:
    """
    Registratiegegevens voor één Paper Trading analyzer.
    """

    name: str
    analyzer: Any


class PaperTradingRegistry:
    """
    Centrale registry voor Paper Trading analyzers.

    De registry bepaalt de deterministische uitvoervolgorde en bevat zelf geen
    trading-, portfolio-, risk- of brokerlogica.
    """

    def __init__(
        self,
        analyzers: list[PaperTradingAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[PaperTradingAnalyzerDefinition]:
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[PaperTradingAnalyzerDefinition]:
        return [
            PaperTradingAnalyzerDefinition(
                name="input_validation",
                analyzer=InputValidationAnalyzer(),
            ),
            PaperTradingAnalyzerDefinition(
                name="trade_execution",
                analyzer=TradeExecutionAnalyzer(),
            ),
            PaperTradingAnalyzerDefinition(
                name="mark_to_market",
                analyzer=MarkToMarketAnalyzer(),
            ),
            PaperTradingAnalyzerDefinition(
                name="position_close",
                analyzer=PositionCloseAnalyzer(),
            ),
            PaperTradingAnalyzerDefinition(
                name="account_summary",
                analyzer=AccountSummaryAnalyzer(),
            ),
        ]
