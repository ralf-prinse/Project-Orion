from __future__ import annotations

from datetime import datetime

from models.paper_portfolio import PaperPortfolio
from models.paper_position import PaperPosition
from models.trade_journal_entry import TradeJournalEntry
from services.dashboard_service import DashboardService


def test_dashboard_service_builds_portfolio_snapshot():
    service = DashboardService()

    portfolio = PaperPortfolio(
        cash=100.0,
        positions={
            "AAA": PaperPosition(
                symbol="AAA",
                quantity=2,
                entry_price=50.0,
                current_price=55.0,
            ),
            "BBB": PaperPosition(
                symbol="BBB",
                quantity=1,
                entry_price=100.0,
                current_price=96.0,
            ),
        },
    )

    journal_entries = [
        TradeJournalEntry(
            timestamp=datetime(2026, 1, 1),
            symbol="CCC",
            action="CLOSE_POSITION",
            decision="TAKE_PROFIT",
            confidence=1.0,
            score=0.0,
            entry_price=100.0,
            exit_price=110.0,
            quantity=1,
            invested_amount=100.0,
            realized_profit_loss=10.0,
            unrealized_profit_loss=0.0,
            expected_risk=0.0,
            regime="UNKNOWN",
            volatility="UNKNOWN",
            ai_summary="Closed test trade.",
            recommendation_reason="Take profit.",
            cycle_number=1,
            session_id="test-session",
        )
    ]

    result = service.build(
        portfolio=portfolio,
        journal_entries=journal_entries,
        initial_cash=500.0,
    )

    assert result.cash == 100.0
    assert result.open_positions == 2
    assert result.open_profit_loss == 6.0
    assert result.closed_profit_loss == 10.0
    assert result.total_profit_loss == 16.0
    assert result.total_return_percent == 3.2
    assert result.closed_trades == 1
    assert result.winning_trades == 1
    assert result.losing_trades == 0
    assert result.winrate_percent == 100.0
    assert len(result.positions) == 2


def main():
    print("\n=========================================")
    print("ORION DASHBOARD SERVICE TEST")
    print("=========================================\n")

    test_dashboard_service_builds_portfolio_snapshot()

    print("DASHBOARD SERVICE: PASS ✅")


if __name__ == "__main__":
    main()