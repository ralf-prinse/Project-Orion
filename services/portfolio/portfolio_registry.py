from dataclasses import dataclass
from typing import Any

from services.portfolio.analyzers.cash_validation_analyzer import CashValidationAnalyzer
from services.portfolio.analyzers.existing_position_analyzer import ExistingPositionAnalyzer
from services.portfolio.analyzers.exposure_analyzer import ExposureAnalyzer
from services.portfolio.analyzers.portfolio_summary_analyzer import PortfolioSummaryAnalyzer
from services.portfolio.analyzers.position_count_analyzer import PositionCountAnalyzer


@dataclass(frozen=True)
class PortfolioAnalyzerDefinition:
    """
    Registratiegegevens voor één portfolio analyzer.
    """

    name: str
    analyzer: Any


class PortfolioRegistry:
    """
    Centrale registry voor alle Portfolio Engine analyzers.

    De registry bepaalt de deterministische uitvoervolgorde en bevat zelf geen
    portfolio- of tradinglogica.
    """

    def __init__(
        self,
        analyzers: list[PortfolioAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[PortfolioAnalyzerDefinition]:
        """
        Retourneert portfolio analyzers in deterministische uitvoervolgorde.
        """
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[PortfolioAnalyzerDefinition]:
        """
        Maakt de standaard Portfolio Engine analyzer-set.
        """
        return [
            PortfolioAnalyzerDefinition(
                name="portfolio_summary",
                analyzer=PortfolioSummaryAnalyzer(),
            ),
            PortfolioAnalyzerDefinition(
                name="cash_validation",
                analyzer=CashValidationAnalyzer(),
            ),
            PortfolioAnalyzerDefinition(
                name="position_count",
                analyzer=PositionCountAnalyzer(),
            ),
            PortfolioAnalyzerDefinition(
                name="existing_position",
                analyzer=ExistingPositionAnalyzer(),
            ),
            PortfolioAnalyzerDefinition(
                name="exposure",
                analyzer=ExposureAnalyzer(),
            ),
        ]
