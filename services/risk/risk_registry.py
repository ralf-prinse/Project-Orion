from dataclasses import dataclass
from typing import Any

from services.risk.analyzers.capital_protection_analyzer import CapitalProtectionAnalyzer
from services.risk.analyzers.drawdown_analyzer import DrawdownAnalyzer
from services.risk.analyzers.portfolio_risk_analyzer import PortfolioRiskAnalyzer
from services.risk.analyzers.position_exposure_risk_analyzer import PositionExposureRiskAnalyzer
from services.risk.analyzers.risk_summary_analyzer import RiskSummaryAnalyzer
from services.risk.analyzers.trade_risk_analyzer import TradeRiskAnalyzer


@dataclass(frozen=True)
class RiskAnalyzerDefinition:
    """
    Registratiegegevens voor één risk analyzer.
    """

    name: str
    analyzer: Any


class RiskRegistry:
    """
    Centrale registry voor Risk Manager analyzers.

    De registry bepaalt de deterministische uitvoervolgorde en bevat zelf geen
    risk-, portfolio- of tradinglogica.
    """

    def __init__(
        self,
        analyzers: list[RiskAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[RiskAnalyzerDefinition]:
        """
        Retourneert risk analyzers in deterministische uitvoervolgorde.
        """
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[RiskAnalyzerDefinition]:
        """
        Maakt de standaard Risk Manager analyzer-set.
        """
        return [
            RiskAnalyzerDefinition(
                name="risk_summary",
                analyzer=RiskSummaryAnalyzer(),
            ),
            RiskAnalyzerDefinition(
                name="trade_risk",
                analyzer=TradeRiskAnalyzer(),
            ),
            RiskAnalyzerDefinition(
                name="portfolio_risk",
                analyzer=PortfolioRiskAnalyzer(),
            ),
            RiskAnalyzerDefinition(
                name="drawdown",
                analyzer=DrawdownAnalyzer(),
            ),
            RiskAnalyzerDefinition(
                name="capital_protection",
                analyzer=CapitalProtectionAnalyzer(),
            ),
            RiskAnalyzerDefinition(
                name="position_exposure_risk",
                analyzer=PositionExposureRiskAnalyzer(),
            ),
        ]
