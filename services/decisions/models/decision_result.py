from dataclasses import dataclass, field

from services.decisions.models.decision_action import DecisionAction
from services.decisions.models.position_sizing_result import PositionSizingResult


@dataclass
class DecisionResult:
    """
    Eindresultaat van de Decision Layer.

    DecisionResult bevat geen indicatoren en geen ruwe analysegegevens.
    Het beschrijft uitsluitend de uiteindelijke investeringsbeslissing.
    """

    symbol: str

    action: DecisionAction = DecisionAction.SKIP
    confidence: int = 0
    position_size: float = 0.0
    risk_level: int = 0
    position_sizing: PositionSizingResult | None = None

    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
