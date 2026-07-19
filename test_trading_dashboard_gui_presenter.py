from datetime import datetime

from models.closed_trade_statistics import ClosedTradeStatistics
from models.trade_journal_entry import TradeJournalEntry
from services.dashboard_service import (
    DashboardPosition,
    DashboardRiskDecision,
    DashboardSnapshot,
)
from ui.foundation.trading_dashboard_gui_presenter import (
    TradingDashboardGuiPresenter,
)


def build_snapshot() -> DashboardSnapshot:
    return DashboardSnapshot(
        cash=47.07,
        equity=505.06,
        open_positions=1,
        open_profit_loss=5.06,
        closed_profit_loss=10.0,
        total_profit_loss=15.06,
        total_return_percent=3.01,
        closed_trades=1,
        winning_trades=1,
        losing_trades=0,
        winrate_percent=100.0,
        positions=[
            DashboardPosition(
                symbol="INTC",
                quantity=1,
                entry_price=105.18,
                current_price=113.29,
                market_value=113.29,
                unrealized_profit_loss=8.11,
                unrealized_return_percent=7.71,
            )
        ],
        closed_trade_statistics=ClosedTradeStatistics(
            closed_trades=1,
            winning_trades=1,
            losing_trades=0,
            winrate_percent=100.0,
            closed_profit_loss=10.0,
            average_winner=10.0,
            average_loser=0.0,
            profit_factor=0.0,
            largest_winner=10.0,
            largest_loser=0.0,
        ),
        risk_decisions=[
            DashboardRiskDecision(
                timestamp="2026-07-09T19:00:00",
                symbol="AMD",
                allowed=False,
                reason="Risk per trade limit exceeded.",
                proposed_risk_ratio=0.02,
                total_portfolio_risk=0.07,
                drawdown=0.03,
                cash_reserve_after_trade=0.40,
                position_exposure=0.10,
            )
        ],
    )


def build_trade() -> TradeJournalEntry:
    return TradeJournalEntry(
        timestamp=datetime(2026, 7, 9, 19, 9, 18),
        symbol="INTC",
        action="OPEN_POSITION",
        decision="BUY",
        confidence=1.0,
        score=0.0,
        entry_price=105.18,
        exit_price=None,
        quantity=1,
        invested_amount=105.18,
        realized_profit_loss=0.0,
        unrealized_profit_loss=0.0,
        expected_risk=0.0,
        regime="UNKNOWN",
        volatility="UNKNOWN",
        ai_summary="Dashboard GUI presenter test.",
        recommendation_reason="Regression test.",
        cycle_number=1,
        session_id="test-session",
    )


def test_trading_dashboard_gui_presenter_creates_workspace():
    presenter = TradingDashboardGuiPresenter()

    workspace = presenter.create_workspace(
        snapshot=build_snapshot(),
        recent_trades=[build_trade()],
    )

    assert workspace.title == "Trading Dashboard"
    assert len(workspace.panels) == 6

    panel_titles = [
        panel.title
        for panel in workspace.panels
    ]

    assert "Portfolio" in panel_titles
    assert "Trading" in panel_titles
    assert "Closed Trade Analytics" in panel_titles
    assert "Open Positions" in panel_titles
    assert "Risk Decisions" in panel_titles
    assert "Recent Trades" in panel_titles

    risk_panel = next(
        panel
        for panel in workspace.panels
        if panel.title == "Risk Decisions"
    )
    assert risk_panel.status == "warning"
    assert any(item["label"] == "AMD" for item in risk_panel.items)


def test_trading_dashboard_gui_presenter_filters_rejected_entries():
    presenter = TradingDashboardGuiPresenter()

    rejected = build_trade()
    rejected = TradeJournalEntry(
        timestamp=rejected.timestamp,
        symbol="AMD",
        action="REJECTED",
        decision="BUY",
        confidence=rejected.confidence,
        score=rejected.score,
        entry_price=rejected.entry_price,
        exit_price=rejected.exit_price,
        quantity=rejected.quantity,
        invested_amount=rejected.invested_amount,
        realized_profit_loss=rejected.realized_profit_loss,
        unrealized_profit_loss=rejected.unrealized_profit_loss,
        expected_risk=rejected.expected_risk,
        regime=rejected.regime,
        volatility=rejected.volatility,
        ai_summary=rejected.ai_summary,
        recommendation_reason=rejected.recommendation_reason,
        cycle_number=rejected.cycle_number,
        session_id=rejected.session_id,
    )

    workspace = presenter.create_workspace(
        snapshot=build_snapshot(),
        recent_trades=[
            rejected,
            build_trade(),
        ],
    )

    recent_panel = workspace.panels[-1]

    assert recent_panel.title == "Recent Trades"
    assert len(recent_panel.items) == 1
    assert recent_panel.items[0]["label"] == "INTC"


def main():
    print("\n=========================================")
    print("ORION TRADING DASHBOARD GUI PRESENTER TEST")
    print("=========================================\n")

    test_trading_dashboard_gui_presenter_creates_workspace()
    test_trading_dashboard_gui_presenter_filters_rejected_entries()

    print("TRADING DASHBOARD GUI PRESENTER: PASS ✅")


if __name__ == "__main__":
    main()
