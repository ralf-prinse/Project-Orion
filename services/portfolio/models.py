from dataclasses import dataclass, field


@dataclass
class PortfolioPosition:
    """
    Eén open positie binnen de Portfolio Engine.

    Dit model bevat alleen portefeuillegegevens. Technische analyse,
    signaallogica en handelsbeslissingen horen hier niet thuis.
    """

    symbol: str
    quantity: int
    average_price: float
    current_price: float | None = None
    sector: str | None = None

    def market_value(self) -> float:
        price = self.current_price if self.current_price is not None else self.average_price
        return round(self.quantity * price, 2)


@dataclass
class PortfolioState:
    """
    Deterministische snapshot van een portefeuille.

    PortfolioState is de standaardinvoer voor de Portfolio Engine. Het model
    bevat geen beslislogica en wijzigt zichzelf niet tijdens analyse.
    """

    cash: float
    positions: dict[str, PortfolioPosition] = field(default_factory=dict)
    currency: str = "USD"

    def total_position_value(self) -> float:
        return round(
            sum(position.market_value() for position in self.positions.values()),
            2,
        )

    def total_value(self) -> float:
        return round(self.cash + self.total_position_value(), 2)

    def open_position_count(self) -> int:
        return sum(
            1
            for position in self.positions.values()
            if position.quantity > 0
        )

    def has_position(self, symbol: str) -> bool:
        position = self.positions.get(symbol.upper())
        return position is not None and position.quantity > 0


@dataclass
class PortfolioContext:
    """
    Configuratie en voorgestelde transactie voor portfolio-validatie.

    De Portfolio Engine gebruikt deze context om te bepalen of een voorgestelde
    positie binnen de portefeuillecapaciteit en exposure-limieten past.
    """

    symbol: str = ""
    proposed_shares: int = 0
    entry_price: float = 0.0
    max_positions: int = 0
    max_position_exposure: float = 0.25
    max_total_exposure: float = 1.0
    allow_existing_position: bool = False

    def proposed_position_value(self) -> float:
        if self.proposed_shares <= 0 or self.entry_price <= 0:
            return 0.0

        return round(self.proposed_shares * self.entry_price, 2)


@dataclass
class PortfolioResult:
    """
    Uitvoer van de Portfolio Engine.

    Dit resultaat is bedoeld als input voor toekomstige Decision Layer-, Risk
    Manager-, Trade Planner- en GUI-integratie.
    """

    symbol: str
    portfolio_value: float = 0.0
    cash_available: float = 0.0
    open_positions: int = 0
    proposed_position_value: float = 0.0
    position_exposure: float = 0.0
    total_exposure: float = 0.0
    cash_sufficient: bool = True
    position_limit_allowed: bool = True
    existing_position_allowed: bool = True
    exposure_allowed: bool = True
    portfolio_allowed: bool = True
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
