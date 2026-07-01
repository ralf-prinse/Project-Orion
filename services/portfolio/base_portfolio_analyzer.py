from abc import ABC, abstractmethod

from services.portfolio.models import PortfolioContext, PortfolioResult, PortfolioState


class BasePortfolioAnalyzer(ABC):
    """
    Basisinterface voor alle Portfolio Engine analyzers.

    Iedere portfolio analyzer:
    - ontvangt PortfolioState
    - ontvangt PortfolioContext
    - verrijkt PortfolioResult
    - blijft volledig deterministisch
    """

    @abstractmethod
    def analyze(
        self,
        portfolio_state: PortfolioState,
        portfolio_context: PortfolioContext,
        portfolio_result: PortfolioResult,
    ) -> PortfolioResult:
        """
        Analyseer portefeuillecontext en verrijk PortfolioResult.
        """
        raise NotImplementedError
