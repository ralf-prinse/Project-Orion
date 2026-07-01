from services.backtesting.models import BacktestResult, BacktestTrade
from services.paper_trading.models import PaperAccount, PaperTradeRecord
from services.performance.models import PerformanceContext, PerformanceTrade
from services.performance.performance_engine import PerformanceEngine


def make_trade(**overrides):
    values = {
        "symbol": "AAPL",
        "entry_price": 100.0,
        "exit_price": 110.0,
        "quantity": 10,
    }
    values.update(overrides)
    return PerformanceTrade(**values)


def test_performance_engine_calculates_core_trade_metrics():
    engine = PerformanceEngine()
    context = PerformanceContext(
        trades=[
            make_trade(exit_price=110.0),  # +100
            make_trade(exit_price=95.0),   # -50
            make_trade(exit_price=105.0),  # +50
            make_trade(exit_price=100.0),  # 0
        ],
        starting_equity=10_000.0,
        label="Strategy A",
    )

    result = engine.run(context)

    assert result.valid_analysis is True
    assert result.label == "Strategy A"
    assert result.total_trades == 4
    assert result.winning_trades == 2
    assert result.losing_trades == 1
    assert result.breakeven_trades == 1
    assert result.win_rate == 50.0
    assert result.loss_rate == 25.0
    assert result.gross_profit == 150.0
    assert result.gross_loss == -50.0
    assert result.net_pnl == 100.0
    assert result.average_win == 75.0
    assert result.average_loss == -50.0
    assert result.average_trade == 25.0
    assert result.expectancy == 25.0
    assert result.profit_factor == 3.0
    assert result.payoff_ratio == 1.5


def test_performance_engine_calculates_equity_curve_and_drawdown():
    engine = PerformanceEngine()
    context = PerformanceContext(
        trades=[
            make_trade(exit_price=110.0),  # equity 10100 peak
            make_trade(exit_price=90.0),   # equity 10000 drawdown 100
            make_trade(exit_price=120.0),  # equity 10200 new peak
        ],
        starting_equity=10_000.0,
    )

    result = engine.run(context)

    assert result.starting_equity == 10_000.0
    assert result.ending_equity == 10_200.0
    assert result.total_return_pct == 2.0
    assert result.max_drawdown_amount == 100.0
    assert result.max_drawdown_pct == 0.99
    assert len(result.equity_curve) == 3
    assert result.equity_curve[1].equity == 10_000.0
    assert result.equity_curve[1].drawdown_amount == 100.0


def test_performance_engine_rejects_empty_trade_list():
    engine = PerformanceEngine()
    context = PerformanceContext(trades=[], starting_equity=10_000.0)

    result = engine.run(context)

    assert result.valid_analysis is False
    assert result.total_trades == 0
    assert result.ending_equity == 10_000.0
    assert "At least one trade is required for performance analytics." in result.warnings


def test_performance_engine_rejects_negative_starting_equity():
    engine = PerformanceEngine()
    context = PerformanceContext(trades=[make_trade()], starting_equity=-1.0)

    result = engine.run(context)

    assert result.valid_analysis is False
    assert "Starting equity must be zero or greater." in result.warnings


def test_performance_engine_rejects_invalid_trade_values():
    engine = PerformanceEngine()
    context = PerformanceContext(
        trades=[make_trade(entry_price=0.0)],
        starting_equity=10_000.0,
    )

    result = engine.run(context)

    assert result.valid_analysis is False
    assert "All trades require positive prices and positive quantity." in result.warnings


def test_performance_engine_derives_starting_equity_when_missing():
    engine = PerformanceEngine()
    context = PerformanceContext(
        trades=[make_trade(entry_price=100.0, quantity=10, exit_price=110.0)],
        starting_equity=0.0,
    )

    result = engine.run(context)

    assert result.starting_equity == 1000.0
    assert result.ending_equity == 1100.0
    assert result.total_return_pct == 10.0


def test_performance_engine_analyzes_backtest_result():
    engine = PerformanceEngine()
    backtest_result = BacktestResult(symbol="AAPL", valid_backtest=True)
    backtest_result.add_trade(
        BacktestTrade(
            symbol="AAPL",
            action="BUY",
            entry_date="2026-01-01",
            entry_price=100.0,
            exit_date="2026-01-05",
            exit_price=112.0,
            shares=10,
            exit_reason="TARGET",
            gross_pnl=120.0,
            return_pct=12.0,
        )
    )

    result = engine.analyze_backtest_result(backtest_result, starting_equity=10_000.0)

    assert result.valid_analysis is True
    assert result.label == "Backtest AAPL"
    assert result.total_trades == 1
    assert result.net_pnl == 120.0
    assert result.ending_equity == 10_120.0


def test_performance_engine_analyzes_closed_paper_trades_only():
    engine = PerformanceEngine()
    account = PaperAccount(starting_cash=5000.0)
    account.trade_history.append(
        PaperTradeRecord(
            symbol="AAPL",
            action="SELL",
            quantity=10,
            entry_price=100.0,
            exit_price=106.0,
            gross_pnl=60.0,
            status="CLOSED",
        )
    )
    account.trade_history.append(
        PaperTradeRecord(
            symbol="MSFT",
            action="BUY",
            quantity=5,
            entry_price=200.0,
            status="OPEN",
        )
    )

    result = engine.analyze_paper_account(account)

    assert result.valid_analysis is True
    assert result.label == "Paper Trading"
    assert result.total_trades == 1
    assert result.net_pnl == 60.0
    assert result.ending_equity == 5060.0


def test_performance_engine_reports_no_closed_paper_trades():
    engine = PerformanceEngine()
    account = PaperAccount(starting_cash=5000.0)

    result = engine.analyze_paper_account(account)

    assert result.valid_analysis is False
    assert "At least one trade is required for performance analytics." in result.warnings
