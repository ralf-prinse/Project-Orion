from services.dashboard_service import (
    DashboardPosition,
    DashboardSnapshot,
)
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
    )

    output = presenter.present(snapshot)

    assert "ORION TRADING DASHBOARD" in output
    assert "Cash" in output
    assert "Equity" in output
    assert "Open P/L" in output
    assert "Closed P/L" in output
    assert "Winrate" in output
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