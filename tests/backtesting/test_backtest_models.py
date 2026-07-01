from services.backtesting.models import BacktestResult, BacktestTrade


def test_backtest_result_adds_trade_and_updates_total():
    result = BacktestResult(symbol="AAPL")
    trade = BacktestTrade(
        symbol="AAPL",
        action="BUY",
        entry_date="2026-01-01",
        entry_price=100.0,
        exit_date="2026-01-05",
        exit_price=110.0,
        shares=10,
        exit_reason="TARGET",
        gross_pnl=100.0,
        return_pct=10.0,
    )

    result.add_trade(trade)

    assert result.total_trades == 1
    assert result.trades == [trade]
    assert trade.is_winner is True


def test_backtest_result_records_reasons_and_warnings():
    result = BacktestResult()

    result.add_reason("reason")
    result.add_warning("warning")

    assert result.reasons == ["reason"]
    assert result.warnings == ["warning"]
