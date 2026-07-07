from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.paper_position_update_service import PaperPositionUpdateService
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

    update_service = PaperPositionUpdateService(
        position_state_store=trading_service.position_state_store,
    )

    update_result = update_service.update_position(
        session=open_result.session,
        symbol="AAPL",
        current_price=112.0,
    )

    print(update_result)

    assert update_result.updated is True
    assert update_result.symbol == "AAPL"

    assert update_result.session.portfolio.positions["AAPL"].current_price == 112.0
    assert update_result.session.portfolio.positions["AAPL"].market_value == 224.0
    assert update_result.session.equity == 1024.0

    assert update_result.position_state is not None
    assert update_result.position_state.current_price == 112.0
    assert update_result.position_state.highest_price == 112.0
    assert update_result.position_state.target_1_hit is True
    assert update_result.position_state.break_even_active is True
    assert update_result.position_state.current_stop_loss > 100.0

    stored = update_service.position_state_store.load("AAPL")

    assert stored is not None
    assert stored.current_price == 112.0

    print("PASS")


if __name__ == "__main__":
    run()