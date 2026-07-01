from services.performance.models import PerformanceTrade


def test_performance_trade_calculates_gross_pnl_when_not_supplied():
    trade = PerformanceTrade(
        symbol="aapl",
        entry_price=100.0,
        exit_price=110.0,
        quantity=5,
    )

    assert trade.normalized_symbol() == "AAPL"
    assert trade.resolved_gross_pnl() == 50.0
    assert trade.position_value() == 500.0
    assert trade.is_winner() is True
    assert trade.is_loser() is False


def test_performance_trade_uses_supplied_gross_pnl():
    trade = PerformanceTrade(
        symbol="MSFT",
        entry_price=100.0,
        exit_price=110.0,
        quantity=5,
        gross_pnl=42.0,
    )

    assert trade.resolved_gross_pnl() == 42.0
