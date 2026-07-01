from abc import ABC, abstractmethod

from services.paper_trading.models import (
    PaperTradingConfig,
    PaperTradingContext,
    PaperTradingResult,
)


class BasePaperTradingAnalyzer(ABC):
    """
    Basisinterface voor Paper Trading analyzers.
    """

    @abstractmethod
    def analyze(
        self,
        paper_trading_context: PaperTradingContext,
        paper_trading_config: PaperTradingConfig,
        paper_trading_result: PaperTradingResult,
    ) -> PaperTradingResult:
        pass
