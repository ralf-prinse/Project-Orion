from services.paper_trading.models import PaperAccount, PaperTradingContext
from services.paper_trading.paper_trading_engine import PaperTradingEngine
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
        "position_value": 1000.0,
        "total_risk_amount": 50.0,
        "currency": "USD",
    }
    values.update(overrides)
    return TradePlanResult(**values)


def test_paper_trading_engine_executes_trade_plan():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)

    result = engine.execute_trade_plan(
        account=account,
        trade_plan=make_trade_plan(),
        timestamp="2026-01-01",
    )

    assert result.valid_operation is True
    assert result.executed_trade.status == "OPEN"
    assert result.cash_balance == 4000.0
    assert result.equity == 5000.0
    assert result.open_positions == 1
    assert account.has_position("AAPL") is True


def test_paper_trading_engine_rejects_invalid_trade_plan():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)

    result = engine.execute_trade_plan(
        account=account,
        trade_plan=make_trade_plan(valid_plan=False),
    )

    assert result.valid_operation is False
    assert result.executed_trade is None
    assert result.open_positions == 0
    assert "Trade plan is not valid; paper trade skipped." in result.warnings


def test_paper_trading_engine_rejects_insufficient_cash():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=500.0)

    result = engine.execute_trade_plan(
        account=account,
        trade_plan=make_trade_plan(),
    )

    assert result.valid_operation is False
    assert result.executed_trade is None
    assert account.open_position_count() == 0
    assert "Paper trade blocked; insufficient cash balance." in result.warnings


def test_paper_trading_engine_rejects_existing_position_by_default():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)

    engine.execute_trade_plan(account=account, trade_plan=make_trade_plan())
    result = engine.execute_trade_plan(account=account, trade_plan=make_trade_plan())

    assert result.valid_operation is False
    assert account.open_position_count() == 1
    assert "Paper trade blocked; position already exists." in result.warnings


def test_paper_trading_engine_marks_to_market_open_positions():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)
    engine.execute_trade_plan(account=account, trade_plan=make_trade_plan())

    result = engine.mark_to_market(
        account=account,
        market_prices={"AAPL": 108.0},
    )

    assert result.valid_operation is True
    assert result.unrealized_pnl == 80.0
    assert result.equity == 5080.0
    assert "Mark-to-market updated 1 open position(s)." in result.reasons


def test_paper_trading_engine_ignores_invalid_mark_to_market_price():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)
    engine.execute_trade_plan(account=account, trade_plan=make_trade_plan())

    result = engine.mark_to_market(
        account=account,
        market_prices={"AAPL": -1.0},
    )

    assert result.valid_operation is True
    assert result.unrealized_pnl == 0.0
    assert "Market price for AAPL ignored; price must be greater than zero." in result.warnings


def test_paper_trading_engine_closes_position():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)
    engine.execute_trade_plan(account=account, trade_plan=make_trade_plan(), timestamp="2026-01-01")

    result = engine.close_position(
        account=account,
        symbol="AAPL",
        close_price=107.0,
        timestamp="2026-01-05",
        close_reason="TARGET",
    )

    assert result.valid_operation is True
    assert result.executed_trade.status == "CLOSED"
    assert result.executed_trade.gross_pnl == 70.0
    assert result.cash_balance == 5070.0
    assert result.realized_pnl == 70.0
    assert result.open_positions == 0


def test_paper_trading_engine_rejects_close_for_missing_position():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)

    result = engine.close_position(
        account=account,
        symbol="AAPL",
        close_price=107.0,
    )

    assert result.valid_operation is False
    assert result.executed_trade is None
    assert "Paper position could not be closed; symbol is not open." in result.warnings


def test_paper_trading_engine_rejects_unsupported_operation():
    engine = PaperTradingEngine()
    account = PaperAccount(starting_cash=5000.0)

    result = engine.run(
        PaperTradingContext(
            account=account,
            operation="UNKNOWN",
        )
    )

    assert result.valid_operation is False
    assert "Unsupported paper-trading operation." in result.warnings
