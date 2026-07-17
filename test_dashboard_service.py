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
        decision_journal_entries=[
            TradeJournalEntry(
                timestamp=datetime(2026, 1, 2),
                symbol="DDD",
                action="REJECTED",
                decision="BUY",
                confidence=0.9,
                score=90.0,
                entry_price=100.0,
                exit_price=None,
                quantity=0,
                invested_amount=0.0,
                realized_profit_loss=0.0,
                unrealized_profit_loss=0.0,
                expected_risk=0.0,
                regime="UNKNOWN",
                volatility="UNKNOWN",
                ai_summary="Risk audit test.",
                recommendation_reason=(
                    "Risk gate rejected allocation; maximum "
                    "drawdown exceeded."
                ),
                cycle_number=1,
                session_id="test-session",
                risk_allowed=False,
                proposed_risk_ratio=0.01,
                total_portfolio_risk=0.04,
                drawdown=0.12,
                cash_reserve_after_trade=0.30,
                position_exposure=0.10,
                risk_warnings=(
                    "Risk validation blocked proposal; "
                    "maximum drawdown exceeded.",
                ),
            )
        ],
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
    assert result.risk_evaluations == 1
    assert result.risk_rejections == 1
    assert result.risk_decisions[0].symbol == "DDD"
    assert result.risk_decisions[0].drawdown == 0.12


def main():
    print("\n=========================================")
    print("ORION DASHBOARD SERVICE TEST")
    print("=========================================\n")

    test_dashboard_service_builds_portfolio_snapshot()

    print("DASHBOARD SERVICE: PASS ✅")


if __name__ == "__main__":
    main()
