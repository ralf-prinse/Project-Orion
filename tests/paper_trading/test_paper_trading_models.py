from services.paper_trading.models import PaperAccount
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
        "total_risk_amount": 50.0,
        "currency": "USD",
    }
    values.update(overrides)
    return TradePlanResult(**values)


def test_paper_account_opens_position_and_reduces_cash():
    account = PaperAccount(starting_cash=5000.0)
    trade_record = account.open_position(make_trade_plan(), timestamp="2026-01-01")

    assert account.cash_balance == 4000.0
    assert account.open_position_count() == 1
    assert account.has_position("AAPL") is True
    assert trade_record.status == "OPEN"
    assert account.equity() == 5000.0


def test_paper_account_updates_market_price_and_unrealized_pnl():
    account = PaperAccount(starting_cash=5000.0)
    account.open_position(make_trade_plan())

    account.update_market_price("AAPL", 108.0)

    assert account.positions["AAPL"].market_value() == 1080.0
    assert account.unrealized_pnl() == 80.0
    assert account.equity() == 5080.0


def test_paper_account_closes_position_and_records_realized_pnl():
    account = PaperAccount(starting_cash=5000.0)
    account.open_position(make_trade_plan(), timestamp="2026-01-01")

    trade_record = account.close_position(
        symbol="AAPL",
        exit_price=107.0,
        timestamp="2026-01-05",
        exit_reason="TARGET",
    )

    assert trade_record.status == "CLOSED"
    assert trade_record.gross_pnl == 70.0
    assert account.open_position_count() == 0
    assert account.cash_balance == 5070.0
    assert account.realized_pnl() == 70.0
    assert account.equity() == 5070.0


def test_paper_account_returns_none_when_closing_missing_position():
    account = PaperAccount(starting_cash=5000.0)

    trade_record = account.close_position("MSFT", 100.0)

    assert trade_record is None
    assert account.cash_balance == 5000.0
