from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.paper_trading_service import PaperTradingService


def run():
    service = PaperTradingService()

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

    result = service.open_position(
        session=session,
        pipeline_output=pipeline_output,
        quantity=2,
    )

    print(result)

    assert result.executed is True
    assert result.symbol == "AAPL"
    assert result.session.cash == 800.0
    assert result.session.open_positions == 1
    assert "AAPL" in result.session.portfolio.positions
    assert "AAPL" in result.session.position_states

    assert result.position_state is not None
    assert result.position_state.symbol == "AAPL"
    assert result.position_state.entry_price == 100.0
    assert result.position_state.current_stop_loss == 95.0

    stored = service.position_state_store.load("AAPL")

    assert stored is not None
    assert stored.symbol == "AAPL"

    print("PASS")


if __name__ == "__main__":
    run()