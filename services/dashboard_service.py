from __future__ import annotations

from dataclasses import dataclass, field

from models.closed_trade_statistics import ClosedTradeStatistics
from models.paper_portfolio import PaperPortfolio
from models.trade_journal_entry import TradeJournalEntry
from services.closed_trade_analytics_service import ClosedTradeAnalyticsService


@dataclass(frozen=True)
class DashboardPosition:
    symbol: str
    quantity: int
    entry_price: float
    current_price: float
    market_value: float
    unrealized_profit_loss: float
    unrealized_return_percent: float


@dataclass(frozen=True)
class DashboardRiskDecision:
    timestamp: str
    symbol: str
    allowed: bool
    reason: str
    proposed_risk_ratio: float | None
    total_portfolio_risk: float | None
    drawdown: float | None
    cash_reserve_after_trade: float | None
    position_exposure: float | None


@dataclass(frozen=True)
class DashboardSnapshot:
    cash: float
    equity: float
    open_positions: int
    open_profit_loss: float
    closed_profit_loss: float
    total_profit_loss: float
    total_return_percent: float
    closed_trades: int
    winning_trades: int
    losing_trades: int
    winrate_percent: float
    positions: list[DashboardPosition]
    closed_trade_statistics: ClosedTradeStatistics
    risk_decisions: list[DashboardRiskDecision] = field(
        default_factory=list
    )

    @property
    def risk_evaluations(self) -> int:
        return len(self.risk_decisions)

    @property
    def risk_rejections(self) -> int:
        return sum(
            not decision.allowed
            for decision in self.risk_decisions
        )


class DashboardService:
    """
    Builds deterministic dashboard snapshots.

    Responsibilities:
    - summarize paper portfolio state
    - summarize closed trade journal statistics
    - expose dashboard-safe data

    Does NOT:
    - load or save data
    - print output
    - make trading decisions
    - mutate portfolio state
    """

    def __init__(
        self,
        closed_trade_analytics_service: (
            ClosedTradeAnalyticsService | None
        ) = None,
    ):
        self.closed_trade_analytics_service = (
            closed_trade_analytics_service
            or ClosedTradeAnalyticsService()
        )

    def build(
        self,
        portfolio: PaperPortfolio,
        journal_entries: list[TradeJournalEntry],
        initial_cash: float,
        decision_journal_entries: (
            list[TradeJournalEntry] | None
        ) = None,
    ) -> DashboardSnapshot:
        positions = [
            self._build_position(symbol, position)
            for symbol, position in portfolio.positions.items()
        ]

        open_profit_loss = round(
            sum(position.unrealized_profit_loss for position in positions),
            2,
        )

        closed_trade_statistics = (
            self.closed_trade_analytics_service.analyze(
                journal_entries=journal_entries,
            )
        )

        total_profit_loss = round(
            open_profit_loss
            + closed_trade_statistics.closed_profit_loss,
            2,
        )

        total_return_percent = (
            round((total_profit_loss / initial_cash) * 100, 2)
            if initial_cash > 0
            else 0.0
        )

        risk_decisions = self._build_risk_decisions(
            decision_journal_entries or [],
        )

        return DashboardSnapshot(
            cash=round(portfolio.cash, 2),
            equity=portfolio.equity,
            open_positions=len(portfolio.positions),
            open_profit_loss=open_profit_loss,
            closed_profit_loss=closed_trade_statistics.closed_profit_loss,
            total_profit_loss=total_profit_loss,
            total_return_percent=total_return_percent,
            closed_trades=closed_trade_statistics.closed_trades,
            winning_trades=closed_trade_statistics.winning_trades,
            losing_trades=closed_trade_statistics.losing_trades,
            winrate_percent=closed_trade_statistics.winrate_percent,
            positions=positions,
            closed_trade_statistics=closed_trade_statistics,
            risk_decisions=risk_decisions,
        )

    def _build_risk_decisions(
        self,
        entries: list[TradeJournalEntry],
    ) -> list[DashboardRiskDecision]:
        decisions: list[DashboardRiskDecision] = []

        for entry in entries:
            is_explicit_risk_gate = (
                entry.recommendation_reason.startswith(
                    "Risk gate rejected allocation;"
                )
            )

            if (
                entry.risk_allowed is None
                and not is_explicit_risk_gate
            ):
                continue

            decisions.append(
                DashboardRiskDecision(
                    timestamp=entry.timestamp.isoformat(),
                    symbol=entry.symbol,
                    allowed=(
                        entry.risk_allowed
                        if entry.risk_allowed is not None
                        else False
                    ),
                    reason=entry.recommendation_reason,
                    proposed_risk_ratio=(
                        entry.proposed_risk_ratio
                    ),
                    total_portfolio_risk=(
                        entry.total_portfolio_risk
                    ),
                    drawdown=entry.drawdown,
                    cash_reserve_after_trade=(
                        entry.cash_reserve_after_trade
                    ),
                    position_exposure=entry.position_exposure,
                )
            )

        return decisions

    def _build_position(
        self,
        symbol,
        position,
    ) -> DashboardPosition:
        unrealized_return_percent = (
            round(
                (
                    (position.current_price - position.entry_price)
                    / position.entry_price
                )
                * 100,
                2,
            )
            if position.entry_price > 0
            else 0.0
        )

        return DashboardPosition(
            symbol=symbol,
            quantity=position.quantity,
            entry_price=position.entry_price,
            current_price=position.current_price,
            market_value=position.market_value,
            unrealized_profit_loss=position.unrealized_profit_loss,
            unrealized_return_percent=unrealized_return_percent,
        )
