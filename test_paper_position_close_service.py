from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.paper_position_close_service import PaperPositionCloseService
from services.paper_trading_service import PaperTradingService


def run():
    session = TradingSession(
        name="Test Session",
        portfolio=PaperPortfolio(cash=1000.0),
    )

    pipeline_output = {
        "symbol": "AAPL",
        "confidence": 0.91,
        "risk_plan": {
            "symbol": "AAPL",
            "entry_price": 100.0,
            "stop_loss": 95.0,
            "target_1": 110.0,
            "target_2": 120.0,
            "target_3": 130.0,
            "risk_percent": 5.0,
            "reward_percent": 10.0,
            "risk_reward_ratio": 2.0,
            "confidence": 0.91,
            "notes": "test",
        },
    }

    opened = PaperTradingService().open_position(
        session=session,
        pipeline_output=pipeline_output,
        quantity=2,
    )

    closed = PaperPositionCloseService().close_position(
        session=opened.session,
        symbol="AAPL",
        exit_price=112.0,
    )

    assert closed.closed is True
    assert closed.realized_profit_loss == 24.0
    assert closed.session.cash == 1024.0
    assert closed.session.portfolio.positions == {}
    assert closed.session.position_states == {}
    assert closed.session.risk_plans == {}
    print("PASS")


if __name__ == "__main__":
    run()
