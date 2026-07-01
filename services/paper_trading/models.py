from dataclasses import dataclass, field
from datetime import date

from services.planner.models import TradePlanResult


@dataclass
class PaperTradingConfig:
    """
    Deterministische configuratie voor de Paper Trading Engine.

    Sprint 8.9 ondersteunt bewust alleen cash accounts, long-only BUY-plannen,
    handmatige sluiting en mark-to-market. Broker-integratie hoort hier niet in.
    """

    allow_existing_position: bool = False
    allow_position_replacement: bool = False
    price_precision: int = 2
    cash_precision: int = 2


@dataclass
class PaperPosition:
    """
    Eén open virtuele positie binnen een paper account.
    """

    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    stop_loss: float = 0.0
    target_price: float = 0.0
    entry_date: date | str = ""
    currency: str = "USD"

    def normalized_symbol(self) -> str:
        return self.symbol.upper()

    def market_value(self) -> float:
        return round(self.quantity * self.current_price, 2)

    def cost_basis(self) -> float:
        return round(self.quantity * self.entry_price, 2)

    def unrealized_pnl(self) -> float:
        return round((self.current_price - self.entry_price) * self.quantity, 2)


@dataclass
class PaperTradeRecord:
    """
    Eén virtueel uitgevoerde transactie binnen paper trading.
    """

    symbol: str
    action: str
    quantity: int
    entry_price: float
    entry_date: date | str = ""
    exit_price: float = 0.0
    exit_date: date | str = ""
    gross_pnl: float = 0.0
    status: str = "OPEN"
    reason: str = ""
    currency: str = "USD"

    def position_value(self) -> float:
        price = self.exit_price if self.status == "CLOSED" else self.entry_price
        return round(self.quantity * price, 2)


@dataclass
class PaperAccount:
    """
    Virtueel account voor paper trading.

    Het account houdt cash, open posities en gesloten trades bij. Het bevat geen
    analyse-, signaal-, beslissing-, risk- of brokerlogica.
    """

    starting_cash: float
    currency: str = "USD"
    cash_balance: float | None = None
    positions: dict[str, PaperPosition] = field(default_factory=dict)
    trade_history: list[PaperTradeRecord] = field(default_factory=list)

    def __post_init__(self):
        if self.cash_balance is None:
            self.cash_balance = round(self.starting_cash, 2)

    def has_position(self, symbol: str) -> bool:
        position = self.positions.get(symbol.upper())
        return position is not None and position.quantity > 0

    def open_position(
        self,
        trade_plan: TradePlanResult,
        timestamp: date | str = "",
        price_precision: int = 2,
        cash_precision: int = 2,
    ) -> PaperTradeRecord:
        symbol = trade_plan.symbol.upper()
        entry_price = round(trade_plan.entry_price, price_precision)
        quantity = trade_plan.shares
        position_value = round(entry_price * quantity, cash_precision)

        self.cash_balance = round(self.cash_balance - position_value, cash_precision)
        self.positions[symbol] = PaperPosition(
            symbol=symbol,
            quantity=quantity,
            entry_price=entry_price,
            current_price=entry_price,
            stop_loss=round(trade_plan.stop_loss, price_precision),
            target_price=round(trade_plan.target_price, price_precision),
            entry_date=timestamp,
            currency=trade_plan.currency,
        )

        trade_record = PaperTradeRecord(
            symbol=symbol,
            action="BUY",
            quantity=quantity,
            entry_price=entry_price,
            entry_date=timestamp,
            status="OPEN",
            reason="TRADE_PLAN_EXECUTION",
            currency=trade_plan.currency,
        )
        return trade_record

    def update_market_price(
        self,
        symbol: str,
        market_price: float,
        price_precision: int = 2,
    ):
        normalized_symbol = symbol.upper()
        if normalized_symbol not in self.positions:
            return

        self.positions[normalized_symbol].current_price = round(market_price, price_precision)

    def close_position(
        self,
        symbol: str,
        exit_price: float,
        timestamp: date | str = "",
        exit_reason: str = "MANUAL",
        price_precision: int = 2,
        cash_precision: int = 2,
    ) -> PaperTradeRecord | None:
        normalized_symbol = symbol.upper()
        position = self.positions.pop(normalized_symbol, None)
        if position is None:
            return None

        rounded_exit_price = round(exit_price, price_precision)
        exit_value = round(rounded_exit_price * position.quantity, cash_precision)
        gross_pnl = round(
            (rounded_exit_price - position.entry_price) * position.quantity,
            cash_precision,
        )
        self.cash_balance = round(self.cash_balance + exit_value, cash_precision)

        trade_record = PaperTradeRecord(
            symbol=normalized_symbol,
            action="SELL",
            quantity=position.quantity,
            entry_price=position.entry_price,
            entry_date=position.entry_date,
            exit_price=rounded_exit_price,
            exit_date=timestamp,
            gross_pnl=gross_pnl,
            status="CLOSED",
            reason=exit_reason,
            currency=position.currency,
        )
        self.trade_history.append(trade_record)
        return trade_record

    def total_position_value(self) -> float:
        return round(sum(position.market_value() for position in self.positions.values()), 2)

    def unrealized_pnl(self) -> float:
        return round(sum(position.unrealized_pnl() for position in self.positions.values()), 2)

    def realized_pnl(self) -> float:
        return round(sum(trade.gross_pnl for trade in self.trade_history if trade.status == "CLOSED"), 2)

    def equity(self) -> float:
        return round(self.cash_balance + self.total_position_value(), 2)

    def open_position_count(self) -> int:
        return sum(1 for position in self.positions.values() if position.quantity > 0)


@dataclass
class PaperTradingContext:
    """
    Invoer voor één registry-gedreven paper-trading operatie.
    """

    account: PaperAccount
    operation: str
    trade_plan: TradePlanResult | None = None
    market_prices: dict[str, float] = field(default_factory=dict)
    close_symbol: str = ""
    close_price: float = 0.0
    close_reason: str = "MANUAL"
    timestamp: date | str = ""

    def normalized_operation(self) -> str:
        return self.operation.strip().upper()

    def normalized_close_symbol(self) -> str:
        return self.close_symbol.strip().upper()


@dataclass
class PaperTradingResult:
    """
    Output van de Paper Trading Engine.
    """

    operation: str
    account: PaperAccount
    valid_operation: bool = True
    executed_trade: PaperTradeRecord | None = None
    cash_balance: float = 0.0
    equity: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    open_positions: int = 0
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_reason(self, reason: str):
        self.reasons.append(reason)

    def add_warning(self, warning: str):
        self.warnings.append(warning)
