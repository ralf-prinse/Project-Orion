from dataclasses import dataclass
from typing import Any

from services.decisions.analyzers.decision_assembler_analyzer import (
    DecisionAssemblerAnalyzer,
)
from services.decisions.analyzers.portfolio_validation_analyzer import (
    PortfolioValidationAnalyzer,
)
from services.decisions.analyzers.position_sizing_analyzer import (
    PositionSizingAnalyzer,
)
from services.decisions.analyzers.risk_validation_analyzer import (
    RiskValidationAnalyzer,
)
from services.decisions.analyzers.signal_validation_analyzer import (
    SignalValidationAnalyzer,
)


@dataclass(frozen=True)
class DecisionAnalyzerDefinition:
    """
    Registratiegegevens voor één decision analyzer.
    """

    name: str
    analyzer: Any


class DecisionRegistry:
    """
    Centrale registry voor alle decision analyzers.

    De registry bepaalt:
    - welke analyzers actief zijn
    - in welke deterministische volgorde ze worden uitgevoerd

    De registry bevat zelf geen beslislogica.
    """

    def __init__(
        self,
        analyzers: list[DecisionAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[DecisionAnalyzerDefinition]:
        """
        Retourneert analyzers in deterministische uitvoervolgorde.
        """
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[DecisionAnalyzerDefinition]:
        """
        Maakt de standaard decision analyzer-set.
        """
        return [
            DecisionAnalyzerDefinition(
                name="signal_validation",
                analyzer=SignalValidationAnalyzer(),
            ),
            DecisionAnalyzerDefinition(
                name="portfolio_validation",
                analyzer=PortfolioValidationAnalyzer(),
            ),
            DecisionAnalyzerDefinition(
                name="risk_validation",
                analyzer=RiskValidationAnalyzer(),
            ),
            DecisionAnalyzerDefinition(
                name="position_sizing",
                analyzer=PositionSizingAnalyzer(),
            ),
            DecisionAnalyzerDefinition(
                name="decision_assembler",
                analyzer=DecisionAssemblerAnalyzer(),
            ),
        ]
