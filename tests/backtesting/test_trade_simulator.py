from services.backtesting.models import BacktestCandle, BacktestConfig
from services.backtesting.trade_simulator import TradeSimulator
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


def test_trade_simulator_exits_at_target():
    simulator = TradeSimulator()
    candles = [
        BacktestCandle("2026-01-01", open=99, high=101, low=98, close=100),
        BacktestCandle("2026-01-02", open=101, high=111, low=100, close=110),
    ]

    trade = simulator.simulate("AAPL", make_trade_plan(), candles, BacktestConfig())

    assert trade is not None
    assert trade.exit_reason == "TARGET"
    assert trade.exit_price == 110.0
    assert trade.gross_pnl == 100.0
    assert trade.return_pct == 10.0


def test_trade_simulator_exits_at_stop_loss():
    simulator = TradeSimulator()
    candles = [
        BacktestCandle("2026-01-01", open=100, high=101, low=99, close=100),
        BacktestCandle("2026-01-02", open=98, high=99, low=94, close=95),
    ]

    trade = simulator.simulate("AAPL", make_trade_plan(), candles, BacktestConfig())

    assert trade is not None
    assert trade.exit_reason == "STOP_LOSS"
    assert trade.exit_price == 95.0
    assert trade.gross_pnl == -50.0
    assert trade.return_pct == -5.0


def test_trade_simulator_uses_conservative_same_candle_exit():
    simulator = TradeSimulator()
    candles = [
        BacktestCandle("2026-01-01", open=100, high=111, low=94, close=106),
    ]

    trade = simulator.simulate("AAPL", make_trade_plan(), candles, BacktestConfig())

    assert trade is not None
    assert trade.exit_reason == "STOP_LOSS"
    assert trade.exit_price == 95.0


def test_trade_simulator_can_use_optimistic_same_candle_exit_when_configured():
    simulator = TradeSimulator()
    candles = [
        BacktestCandle("2026-01-01", open=100, high=111, low=94, close=106),
    ]

    trade = simulator.simulate(
        "AAPL",
        make_trade_plan(),
        candles,
        BacktestConfig(conservative_same_candle_exit=False),
    )

    assert trade is not None
    assert trade.exit_reason == "TARGET"
    assert trade.exit_price == 110.0


def test_trade_simulator_closes_at_end_of_data_when_no_exit_hit():
    simulator = TradeSimulator()
    candles = [
        BacktestCandle("2026-01-01", open=100, high=101, low=99, close=100),
        BacktestCandle("2026-01-02", open=102, high=105, low=101, close=104),
    ]

    trade = simulator.simulate("AAPL", make_trade_plan(), candles, BacktestConfig())

    assert trade is not None
    assert trade.exit_reason == "END_OF_DATA"
    assert trade.exit_price == 104.0
    assert trade.gross_pnl == 40.0


def test_trade_simulator_returns_none_when_entry_not_reached():
    simulator = TradeSimulator()
    candles = [
        BacktestCandle("2026-01-01", open=105, high=110, low=104, close=109),
    ]

    trade = simulator.simulate("AAPL", make_trade_plan(), candles, BacktestConfig())

    assert trade is None


def test_trade_simulator_ignores_non_buy_plans():
    simulator = TradeSimulator()
    candles = [BacktestCandle("2026-01-01", open=100, high=101, low=99, close=100)]

    trade = simulator.simulate(
        "AAPL",
        make_trade_plan(action="HOLD"),
        candles,
        BacktestConfig(),
    )

    assert trade is None
