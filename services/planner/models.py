from dataclasses import dataclass, field


@dataclass
class TradePlannerConfig:
    """
    Deterministische configuratie voor de Trade Planner.

    De configuratie bevat uitsluitend planningsgrenzen. Portfolio- en
    risk-validatie horen in hun eigen lagen en worden hier niet opnieuw
    uitgevoerd.
    """

    default_reward_risk_ratio: float = 2.0
    minimum_reward_risk_ratio: float = 1.5
    price_precision: int = 2


@dataclass
class TradePlanContext:
    """
    Invoer voor één handelsplan.

    De Trade Planner gebruikt reeds goedgekeurde, deterministische inputs uit
    eerdere lagen zoals Decision Layer, Position Sizing, Portfolio Engine en
    Risk Manager. De planner neemt zelf geen investeringsbeslissing.
    """

    symbol: str
    action: str
    entry_price: float
    stop_loss: float
    recommended_shares: int
    target_price: float | None = None
    risk_amount: float = 0.0
    currency: str = "USD"
    notes: list[str] = field(default_factory=list)

    def normalized_action(self) -> str:
        return str(self.action).strip().upper()


@dataclass
class TradePlanResult:
    """
    Uitvoer van de Trade Planner.

    TradePlanResult is bedoeld voor GUI, rapportages, paper trading en latere
    broker-integraties. Het model bevat geen technische analyse, portfolio- of
    risk-managementlogica.
    """

    symbol: str = ""
    action: str = "NONE"
    valid_plan: bool = False
    entry_price: float = 0.0
    stop_loss: float = 0.0
    target_price: float = 0.0
    shares: int = 0
    position_value: float = 0.0
    risk_per_share: float = 0.0
    total_risk_amount: float = 0.0
    expected_reward_per_share: float = 0.0
    expected_reward_amount: float = 0.0
    reward_risk_ratio: float = 0.0
    currency: str = "USD"
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
