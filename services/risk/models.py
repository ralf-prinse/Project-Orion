from dataclasses import dataclass, field


@dataclass
class RiskProfile:
    """
    Deterministisch risicoprofiel voor de Risk Manager.

    Dit profiel bevat uitsluitend grenswaarden. Het neemt geen technische,
    portfolio- of trade-planningbeslissingen.
    """

    max_risk_per_trade: float = 0.01
    max_portfolio_risk: float = 0.06
    max_drawdown: float = 0.10
    min_cash_reserve: float = 0.10
    max_position_exposure: float = 0.25


@dataclass
class RiskContext:
    """
    Invoercontext voor één risk-evaluatie.

    De Risk Manager gebruikt deze waarden om voorgestelde trades en bestaande
    portefeuillerisico's te toetsen aan een RiskProfile.
    """

    symbol: str = ""
    portfolio_value: float = 0.0
    cash_available: float = 0.0
    current_portfolio_risk: float = 0.0
    proposed_position_value: float = 0.0
    proposed_risk_amount: float = 0.0
    peak_portfolio_value: float = 0.0
    current_drawdown: float | None = None

    def proposed_risk_ratio(self) -> float:
        if self.portfolio_value <= 0 or self.proposed_risk_amount <= 0:
            return 0.0
        return round(self.proposed_risk_amount / self.portfolio_value, 4)

    def proposed_position_exposure(self) -> float:
        if self.portfolio_value <= 0 or self.proposed_position_value <= 0:
            return 0.0
        return round(self.proposed_position_value / self.portfolio_value, 4)

    def total_portfolio_risk(self) -> float:
        return round(self.current_portfolio_risk + self.proposed_risk_ratio(), 4)

    def cash_reserve_after_trade(self) -> float:
        if self.portfolio_value <= 0:
            return 0.0
        remaining_cash = self.cash_available - self.proposed_position_value
        return round(remaining_cash / self.portfolio_value, 4)

    def drawdown_ratio(self) -> float:
        if self.current_drawdown is not None:
            return round(max(self.current_drawdown, 0.0), 4)

        if self.peak_portfolio_value <= 0 or self.portfolio_value <= 0:
            return 0.0

        drawdown = (self.peak_portfolio_value - self.portfolio_value) / self.peak_portfolio_value
        return round(max(drawdown, 0.0), 4)


@dataclass
class RiskResult:
    """
    Uitvoer van de Risk Manager.

    RiskResult is bedoeld voor latere integratie met Decision Layer,
    Portfolio Engine, Trade Planner, GUI en rapportage.
    """

    symbol: str = ""
    risk_allowed: bool = True
    portfolio_value: float = 0.0
    proposed_risk_ratio: float = 0.0
    total_portfolio_risk: float = 0.0
    drawdown: float = 0.0
    cash_reserve_after_trade: float = 0.0
    position_exposure: float = 0.0
    trade_risk_allowed: bool = True
    portfolio_risk_allowed: bool = True
    drawdown_allowed: bool = True
    capital_protection_allowed: bool = True
    position_exposure_allowed: bool = True
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
