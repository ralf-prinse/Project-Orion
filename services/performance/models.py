from dataclasses import dataclass, field
from datetime import date


@dataclass
class PerformanceConfig:
    """
    Deterministische configuratie voor Performance Analytics.

    Deze laag berekent uitsluitend statistieken over reeds uitgevoerde of
    gesimuleerde trades. De configuratie bepaalt alleen afronding en niet de
    tradinglogica zelf.
    """

    currency: str = "USD"
    cash_precision: int = 2
    percentage_precision: int = 2
    ratio_precision: int = 2


@dataclass(frozen=True)
class PerformanceTrade:
    """
    Gestandaardiseerde trade-input voor Performance Analytics.

    Dit model is bewust losgekoppeld van BacktestTrade en PaperTradeRecord,
    zodat backtesting, paper trading en latere broker-integraties dezelfde
    analytics-laag kunnen gebruiken zonder domeinlogica te dupliceren.
    """

    symbol: str
    entry_price: float
    exit_price: float
    quantity: int
    entry_date: date | str = ""
    exit_date: date | str = ""
    gross_pnl: float | None = None
    currency: str = "USD"

    def normalized_symbol(self) -> str:
        return self.symbol.strip().upper()

    def resolved_gross_pnl(self) -> float:
        if self.gross_pnl is not None:
            return float(self.gross_pnl)
        return (self.exit_price - self.entry_price) * self.quantity

    def position_value(self) -> float:
        return self.entry_price * self.quantity

    def is_winner(self) -> bool:
        return self.resolved_gross_pnl() > 0

    def is_loser(self) -> bool:
        return self.resolved_gross_pnl() < 0


@dataclass(frozen=True)
class EquityCurvePoint:
    """
    Eén punt op de deterministische equity curve.
    """

    index: int
    equity: float
    drawdown_amount: float
    drawdown_pct: float


@dataclass
class PerformanceContext:
    """
    Invoer voor Performance Analytics.

    Sprint 9.0 analyseert trade-resultaten. Deze laag genereert geen trades en
    voert geen portfolio- of risk-beslissingen uit.
    """

    trades: list[PerformanceTrade] = field(default_factory=list)
    starting_equity: float = 0.0
    label: str = ""


@dataclass
class PerformanceResult:
    """
    Professionele performance-output voor backtests, paper trading, rapportages,
    GUI en toekomstige AI-uitleg.
    """

    label: str = ""
    valid_analysis: bool = False
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    breakeven_trades: int = 0
    win_rate: float = 0.0
    loss_rate: float = 0.0
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    net_pnl: float = 0.0
    average_win: float = 0.0
    average_loss: float = 0.0
    average_trade: float = 0.0
    expectancy: float = 0.0
    profit_factor: float = 0.0
    payoff_ratio: float = 0.0
    starting_equity: float = 0.0
    ending_equity: float = 0.0
    total_return_pct: float = 0.0
    max_drawdown_amount: float = 0.0
    max_drawdown_pct: float = 0.0
    equity_curve: list[EquityCurvePoint] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
