from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from services.paper_trading_service import PaperTradingService
from services.position_state_store import PositionStateStore
from services.trading_cycle import TradingCycle


def build_pipeline_output() -> dict:
    return {
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
            "reward_percent": 30.0,
            "risk_reward_ratio": 6.0,
            "confidence": 0.91,
            "notes": "PositionStateStore lifecycle synchronization test.",
        },
    }


def test_shared_position_state_store_stays_synchronized():
    shared_store = PositionStateStore()

    paper_trading_service = PaperTradingService(
        position_state_store=shared_store,
    )

    cycle = TradingCycle(
        paper_trading_service=paper_trading_service,
    )

    session = TradingSession(
        name="Position State Store Synchronization Test",
        portfolio=PaperPortfolio(
            cash=1000.0,
        ),
    )

    open_result = cycle.run(
        session=session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
            pipeline_output=build_pipeline_output(),
        ),
        quantity=2,
    )

    assert open_result.action == "OPEN_POSITION"
    assert open_result.session.portfolio.cash == 800.0
    assert "AAPL" in open_result.session.portfolio.positions
    assert "AAPL" in open_result.session.position_states
    assert "AAPL" in open_result.session.risk_plans

    stored_after_open = shared_store.load("AAPL")

    assert stored_after_open is not None
    assert stored_after_open.current_price == 100.0
    assert stored_after_open.current_stop_loss == 95.0

    update_result = cycle.run(
        session=open_result.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=112.0,
        ),
    )

    assert update_result.action == "UPDATE_POSITION"
    assert "AAPL" in update_result.session.portfolio.positions
    assert "AAPL" in update_result.session.position_states
    assert "AAPL" in update_result.session.risk_plans

    session_state = update_result.session.position_states["AAPL"]
    stored_after_update = shared_store.load("AAPL")

    assert stored_after_update is not None
    assert stored_after_update == session_state
    assert stored_after_update.current_price == 112.0
    assert stored_after_update.highest_price == 112.0
    assert stored_after_update.target_1_hit is True
    assert stored_after_update.break_even_active is True
    assert stored_after_update.trailing_stop_active is True
    assert stored_after_update.current_stop_loss == 106.4

    close_result = cycle.run(
        session=update_result.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=106.0,
        ),
    )

    assert close_result.action == "CLOSE_POSITION"
    assert close_result.session.portfolio.cash == 1012.0
    assert "AAPL" not in close_result.session.portfolio.positions
    assert "AAPL" not in close_result.session.position_states
    assert "AAPL" not in close_result.session.risk_plans
    assert shared_store.load("AAPL") is None


def main():
    print()
    print("=========================================")
    print("POSITION STATE STORE LIFECYCLE SYNC TEST")
    print("=========================================")
    print()

    test_shared_position_state_store_stays_synchronized()

    print("POSITION STATE STORE LIFECYCLE SYNC: PASS")


if __name__ == "__main__":
    main()
