from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.paper_position_close_service import PaperPositionCloseService
from services.paper_trading_service import PaperTradingService


def run():
    trading_service = PaperTradingService()

    session = TradingSession(
        name="Test Session",
        portfolio=PaperPortfolio(
            cash=1000.0,
        ),
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

    open_result = trading_service.open_position(
        session=session,
        pipeline_output=pipeline_output,
        quantity=2,
    )

    close_service = PaperPositionCloseService(
        position_state_store=trading_service.position_state_store,
    )

    close_result = close_service.close_position(
        session=open_result.session,
        symbol="AAPL",
        exit_price=112.0,
    )

    print(close_result)

    assert close_result.closed is True
    assert close_result.symbol == "AAPL"
    assert close_result.realized_profit_loss == 24.0
    assert close_result.session.cash == 1024.0
    assert close_result.session.open_positions == 0
    assert "AAPL" not in close_result.session.portfolio.positions
    assert "AAPL" not in close_result.session.position_states
    assert "AAPL" not in close_result.session.risk_plans

    stored = close_service.position_state_store.load("AAPL")

    assert stored is None

    print("PASS")


if __name__ == "__main__":
    run()