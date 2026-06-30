from dataclasses import dataclass
from typing import Any

from services.analysis.analyzers.candlestick_pattern_analyzer import (
    CandlestickPatternAnalyzer,
)
from services.analysis.analyzers.market_regime_analyzer import MarketRegimeAnalyzer
from services.analysis.analyzers.momentum_analyzer import MomentumAnalyzer
from services.analysis.analyzers.relative_strength_analyzer import (
    RelativeStrengthAnalyzer,
)
from services.analysis.analyzers.structure_analyzer import StructureAnalyzer
from services.analysis.analyzers.trend_analyzer import TrendAnalyzer
from services.analysis.analyzers.volatility_analyzer import VolatilityAnalyzer
from services.analysis.analyzers.volume_analyzer import VolumeAnalyzer


@dataclass(frozen=True)
class AnalyzerDefinition:
    """
    Registratiegegevens voor één analyzer binnen de Analysis Layer.
    """

    name: str
    analyzer: Any
    score_field: str
    uses_candles: bool = False
    contributes_to_overall: bool = True


class AnalyzerRegistry:
    """
    Centrale registry voor alle analyzers binnen de Analysis Layer.

    De registry bepaalt:
    - welke analyzers actief zijn
    - in welke vaste volgorde ze worden uitgevoerd
    - welk scoreveld ze vullen
    - of raw candledata nodig is
    - of ze meetellen in de overall technische score

    De registry voert zelf geen analyse uit.
    """

    def __init__(
        self,
        analyzers: list[AnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[AnalyzerDefinition]:
        """
        Retourneert analyzers in deterministische uitvoervolgorde.
        """
        return list(self._analyzers)

    def get_overall_score_analyzers(self) -> list[AnalyzerDefinition]:
        """
        Retourneert alleen analyzers die meetellen in de overall score.
        """
        return [
            analyzer_definition
            for analyzer_definition in self._analyzers
            if analyzer_definition.contributes_to_overall
        ]

    def _create_default_analyzers(self) -> list[AnalyzerDefinition]:
        """
        Maakt de standaard analyzer-set voor Project Orion.
        """
        return [
            AnalyzerDefinition(
                name="trend",
                analyzer=TrendAnalyzer(),
                score_field="trend_score",
            ),
            AnalyzerDefinition(
                name="momentum",
                analyzer=MomentumAnalyzer(),
                score_field="momentum_score",
            ),
            AnalyzerDefinition(
                name="volatility",
                analyzer=VolatilityAnalyzer(),
                score_field="volatility_score",
            ),
            AnalyzerDefinition(
                name="structure",
                analyzer=StructureAnalyzer(),
                score_field="structure_score",
            ),
            AnalyzerDefinition(
                name="volume",
                analyzer=VolumeAnalyzer(),
                score_field="volume_score",
            ),
            AnalyzerDefinition(
                name="market_regime",
                analyzer=MarketRegimeAnalyzer(),
                score_field="market_regime_score",
                contributes_to_overall=False,
            ),
            AnalyzerDefinition(
                name="relative_strength",
                analyzer=RelativeStrengthAnalyzer(),
                score_field="relative_strength_score",
            ),
            AnalyzerDefinition(
                name="candlestick",
                analyzer=CandlestickPatternAnalyzer(),
                score_field="candlestick_score",
                uses_candles=True,
            ),
        ]