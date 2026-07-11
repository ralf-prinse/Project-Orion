from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.paper_position_update_service import PaperPositionUpdateService
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

    updated = PaperPositionUpdateService().update_position(
        session=opened.session,
        symbol="AAPL",
        current_price=112.0,
    )

    assert updated.updated is True
    assert updated.session.portfolio.positions["AAPL"].current_price == 112.0
    assert updated.session.equity == 1024.0
    assert updated.position_state is not None
    assert updated.session.position_states["AAPL"] == updated.position_state
    print("PASS")


if __name__ == "__main__":
    run()
