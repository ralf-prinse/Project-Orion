from dataclasses import dataclass
from typing import Any

from services.signals.analyzers.entry_signal_analyzer import EntrySignalAnalyzer


@dataclass(frozen=True)
class SignalAnalyzerDefinition:
    """
    Registratiegegevens voor één signal analyzer.
    """

    name: str
    analyzer: Any


class SignalRegistry:
    """
    Centrale registry voor alle signal analyzers binnen de Signal Layer.

    De registry bepaalt:
    - welke signal analyzers actief zijn
    - in welke deterministische volgorde ze worden uitgevoerd

    De registry bevat zelf geen signaallogica.
    """

    def __init__(
        self,
        analyzers: list[SignalAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[SignalAnalyzerDefinition]:
        """
        Retourneert signal analyzers in deterministische uitvoervolgorde.
        """
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[SignalAnalyzerDefinition]:
        """
        Maakt de standaard signal analyzer-set voor Project Orion.
        """
        return [
            SignalAnalyzerDefinition(
                name="entry",
                analyzer=EntrySignalAnalyzer(),
            )
        ]