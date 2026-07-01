from dataclasses import dataclass, field


@dataclass
class PositionSizingResult:
    """
    Deterministisch resultaat van de Position Sizing-berekening.

    Dit model bevat uitsluitend sizing-informatie. Het bepaalt niet of een
    positie geopend mag worden en bevat geen portfolio- of trade-planninglogica.
    """

    recommended_shares: int = 0
    position_value: float = 0.0
    risk_amount: float = 0.0
    risk_per_share: float = 0.0
    capital_used: float = 0.0
    sizing_method: str = "fixed_fractional_risk"
    warnings: list[str] = field(default_factory=list)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
