from dataclasses import dataclass, field

from services.decisions.models.decision_action import DecisionAction


@dataclass
class DecisionState:
    """
    Interne state die door decision analyzers wordt opgebouwd.

    Elke analyzer mag één duidelijk afgebakend deel van de state verrijken.
    De uiteindelijke DecisionResult wordt later uit deze state samengesteld.
    """

    symbol: str

    signal_valid: bool = False
    portfolio_allowed: bool = True
    risk_allowed: bool = True

    proposed_action: DecisionAction = DecisionAction.SKIP
    confidence: int = 0
    position_size: float = 0.0
    risk_level: int = 0

    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)