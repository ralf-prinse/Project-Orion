from dataclasses import dataclass
from typing import Any

from services.planner.analyzers.input_validation_analyzer import InputValidationAnalyzer
from services.planner.analyzers.risk_reward_analyzer import RiskRewardAnalyzer
from services.planner.analyzers.target_price_analyzer import TargetPriceAnalyzer
from services.planner.analyzers.trade_plan_summary_analyzer import TradePlanSummaryAnalyzer


@dataclass(frozen=True)
class TradePlanAnalyzerDefinition:
    """
    Registratiegegevens voor één Trade Planner analyzer.
    """

    name: str
    analyzer: Any


class TradePlanRegistry:
    """
    Centrale registry voor Trade Planner analyzers.

    De registry bepaalt de deterministische uitvoervolgorde en bevat zelf geen
    handels-, portfolio- of risklogica.
    """

    def __init__(
        self,
        analyzers: list[TradePlanAnalyzerDefinition] | None = None,
    ):
        self._analyzers = analyzers or self._create_default_analyzers()

    def get_analyzers(self) -> list[TradePlanAnalyzerDefinition]:
        return list(self._analyzers)

    def _create_default_analyzers(self) -> list[TradePlanAnalyzerDefinition]:
        return [
            TradePlanAnalyzerDefinition(
                name="input_validation",
                analyzer=InputValidationAnalyzer(),
            ),
            TradePlanAnalyzerDefinition(
                name="target_price",
                analyzer=TargetPriceAnalyzer(),
            ),
            TradePlanAnalyzerDefinition(
                name="risk_reward",
                analyzer=RiskRewardAnalyzer(),
            ),
            TradePlanAnalyzerDefinition(
                name="trade_plan_summary",
                analyzer=TradePlanSummaryAnalyzer(),
            ),
        ]
