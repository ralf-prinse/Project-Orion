from services.dashboard_service import (
    DashboardPosition,
    DashboardRiskDecision,
    DashboardSnapshot,
)
from models.closed_trade_statistics import ClosedTradeStatistics
from ui.foundation.trading_dashboard_cli_presenter import (
    TradingDashboardCliPresenter,
)


def test_trading_dashboard_cli_presenter_formats_snapshot():
    presenter = TradingDashboardCliPresenter()

    snapshot = DashboardSnapshot(
        cash=205.52,
        equity=500.0,
        open_positions=1,
        open_profit_loss=12.5,
        closed_profit_loss=8.25,
        total_profit_loss=20.75,
        total_return_percent=4.15,
        closed_trades=2,
        winning_trades=1,
        losing_trades=1,
        winrate_percent=50.0,
        positions=[
            DashboardPosition(
                symbol="NFLX",
                quantity=1,
                entry_price=75.88,
                current_price=88.38,
                market_value=88.38,
                unrealized_profit_loss=12.5,
                unrealized_return_percent=16.47,
            )
        ],
        closed_trade_statistics=ClosedTradeStatistics(
            closed_trades=2,
            winning_trades=1,
            losing_trades=1,
            winrate_percent=50.0,
            closed_profit_loss=8.25,
            average_winner=15.0,
            average_loser=-6.75,
            profit_factor=2.22,
            largest_winner=15.0,
            largest_loser=-6.75,
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

    output = presenter.present(snapshot)

    assert "ORION TRADING DASHBOARD" in output
    assert "Cash" in output
    assert "Equity" in output
    assert "Open P/L" in output
    assert "Closed P/L" in output
    assert "Winrate" in output
    assert "CLOSED TRADE ANALYTICS" in output
    assert "Average Winner" in output
    assert "Profit Factor" in output
    assert "RISK DECISIONS" in output
    assert "AMD" in output
    assert "BLOCKED" in output
    assert "NFLX" in output
    assert "€   12.50" in output


def main():
    print("\n=========================================")
    print("ORION TRADING DASHBOARD CLI PRESENTER TEST")
    print("=========================================\n")

    test_trading_dashboard_cli_presenter_formats_snapshot()

    print("TRADING DASHBOARD CLI PRESENTER: PASS ✅")


if __name__ == "__main__":
    main()
