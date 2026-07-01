from dataclasses import dataclass, field
from datetime import date

from services.planner.models import TradePlanResult


@dataclass(frozen=True)
class BacktestCandle:
    """
    Eén historische candle voor deterministische backtesting.

    De Backtesting Layer gebruikt reeds gevalideerde historische data. Dit model
    bevat alleen de OHLCV-waarden die nodig zijn om een bestaand handelsplan te
    simuleren.
    """

    timestamp: date | str
    open: float
    high: float
    low: float
    close: float
    volume: int = 0


@dataclass
class BacktestConfig:
    """
    Configuratie voor de Backtesting Foundation.

    De standaard is bewust conservatief: wanneer stop-loss en target in dezelfde
    candle geraakt worden, wordt de stop-loss eerst uitgevoerd. Dat voorkomt dat
    Orion optimistische aannames maakt over intraday volgorde binnen daily data.
    """

    conservative_same_candle_exit: bool = True
    price_precision: int = 2
    percentage_precision: int = 2


@dataclass
class BacktestContext:
    """
    Invoer voor één deterministische backtest.

    Sprint 8.8 simuleert bewust een bestaand TradePlanResult. De Backtesting
    Layer genereert dus zelf geen signalen, beslissingen of handelsplannen.
    """

    trade_plan: TradePlanResult
    candles: list[BacktestCandle]
    symbol: str = ""
    initial_capital: float = 0.0

    def resolved_symbol(self) -> str:
        return (self.symbol or self.trade_plan.symbol).upper()


@dataclass
class BacktestTrade:
    """
    Uitgevoerde gesimuleerde trade binnen een backtest.
    """

    symbol: str
    action: str
    entry_date: date | str
    entry_price: float
    exit_date: date | str
    exit_price: float
    shares: int
    exit_reason: str
    gross_pnl: float
    return_pct: float

    @property
    def is_winner(self) -> bool:
        return self.gross_pnl > 0


@dataclass
class BacktestResult:
    """
    Output van de Backtesting Engine.

    Het resultaat is geschikt voor rapportages, performance analytics, GUI en
    toekomstige AI-uitleg. Het bevat geen live portfolio-mutaties en geen broker-
    integratie.
    """

    symbol: str = ""
    valid_backtest: bool = False
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_gross_pnl: float = 0.0
    total_return_pct: float = 0.0
    max_drawdown: float = 0.0
    trades: list[BacktestTrade] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_trade(self, trade: BacktestTrade):
        self.trades.append(trade)
        self.total_trades = len(self.trades)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
