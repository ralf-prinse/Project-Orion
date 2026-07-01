from services.backtesting.backtest_engine import BacktestEngine
from services.backtesting.models import BacktestCandle, BacktestContext
from services.planner.models import TradePlanResult


def make_trade_plan(**overrides):
    values = {
        "symbol": "AAPL",
        "action": "BUY",
        "valid_plan": True,
        "entry_price": 100.0,
        "stop_loss": 95.0,
        "target_price": 110.0,
        "shares": 10,
    }
    values.update(overrides)
    return TradePlanResult(**values)


def test_backtest_engine_runs_successful_backtest():
    engine = BacktestEngine()
    context = BacktestContext(
        trade_plan=make_trade_plan(),
        candles=[
            BacktestCandle("2026-01-01", open=99, high=101, low=98, close=100),
            BacktestCandle("2026-01-02", open=104, high=111, low=103, close=110),
        ],
        initial_capital=10_000,
    )

    result = engine.run(context)

    assert result.valid_backtest is True
    assert result.symbol == "AAPL"
    assert result.total_trades == 1
    assert result.winning_trades == 1
    assert result.losing_trades == 0
    assert result.win_rate == 100.0
    assert result.total_gross_pnl == 100.0
    assert result.total_return_pct == 1.0
    assert result.max_drawdown == 0.0
    assert result.trades[0].exit_reason == "TARGET"


def test_backtest_engine_rejects_invalid_trade_plan():
    engine = BacktestEngine()
    context = BacktestContext(
        trade_plan=make_trade_plan(valid_plan=False),
        candles=[BacktestCandle("2026-01-01", open=99, high=101, low=98, close=100)],
    )

    result = engine.run(context)

    assert result.valid_backtest is False
    assert "Trade plan is not valid; backtest skipped." in result.warnings
    assert result.total_trades == 0


def test_backtest_engine_rejects_empty_candles():
    engine = BacktestEngine()
    context = BacktestContext(
        trade_plan=make_trade_plan(),
        candles=[],
    )

    result = engine.run(context)

    assert result.valid_backtest is False
    assert "At least one candle is required for backtesting." in result.warnings


def test_backtest_engine_reports_entry_not_reached():
    engine = BacktestEngine()
    context = BacktestContext(
        trade_plan=make_trade_plan(),
        candles=[BacktestCandle("2026-01-01", open=105, high=106, low=104, close=105)],
    )

    result = engine.run(context)

    assert result.valid_backtest is False
    assert "Entry price was not reached during the backtest period." in result.warnings
    assert result.total_trades == 0
