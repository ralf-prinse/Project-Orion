from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.position_state import PositionState
from models.trading_session import TradingSession
from services.paper_position_close_service import (
    PaperPositionCloseService,
)
from services.paper_position_update_service import (
    PaperPositionUpdateService,
)
from services.paper_trading_service import PaperTradingService
from services.position_state_store import PositionStateStore
from services.trading_cycle import TradingCycle


class AuditedPositionStateStore(PositionStateStore):
    def __init__(self):
        super().__init__()
        self.save_calls = 0
        self.load_calls = 0
        self.remove_calls = 0

    def save(self, state: PositionState) -> None:
        self.save_calls += 1
        super().save(state)

    def load(self, symbol: str) -> PositionState | None:
        self.load_calls += 1
        return super().load(symbol)

    def remove(self, symbol: str) -> None:
        self.remove_calls += 1
        super().remove(symbol)


def _pipeline_output(symbol: str, entry: float) -> dict:
    return {
        "symbol": symbol,
        "confidence": 0.91,
        "risk_plan": {
            "symbol": symbol,
            "entry_price": entry,
            "stop_loss": entry * 0.95,
            "target_1": entry * 1.10,
            "target_2": entry * 1.20,
            "target_3": entry * 1.30,
            "risk_percent": 5.0,
            "reward_percent": 10.0,
            "risk_reward_ratio": 2.0,
            "confidence": 0.91,
            "notes": "PositionStateStore ownership audit.",
        },
    }


def test_runtime_uses_session_as_read_source_and_store_as_write_mirror():
    store = AuditedPositionStateStore()

    paper_trading_service = PaperTradingService(
        position_state_store=store,
    )
    update_service = PaperPositionUpdateService(
        position_state_store=store,
    )
    close_service = PaperPositionCloseService(
        position_state_store=store,
    )

    cycle = TradingCycle(
        paper_trading_service=paper_trading_service,
        update_service=update_service,
        close_service=close_service,
    )

    session = TradingSession(
        name="PositionStateStore Ownership Audit",
        portfolio=PaperPortfolio(cash=1000.0),
    )

    opened = cycle.run(
        session=session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
            pipeline_output=_pipeline_output("AAPL", 100.0),
        ),
        quantity=2,
    )

    assert opened.action == "OPEN_POSITION"
    assert "AAPL" in opened.session.position_states
    assert store.save_calls == 1
    assert store.load_calls == 0

    updated = cycle.run(
        session=opened.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=112.0,
        ),
    )

    assert updated.action == "UPDATE_POSITION"
    assert updated.session.position_states["AAPL"].current_price == 112.0
    assert store.save_calls == 2
    assert store.load_calls == 0

    closed = cycle.run(
        session=updated.session,
        snapshot=MarketSnapshot(
            symbol="AAPL",
            current_price=100.0,
        ),
    )

    assert closed.action == "CLOSE_POSITION"
    assert closed.session.position_states == {}
    assert closed.session.risk_plans == {}
    assert store.remove_calls == 1
    assert store.load_calls == 0

    # Explicit verification reads are test-only and not part of runtime flow.
    assert store.load("AAPL") is None
    assert store.load_calls == 1


def main():
    print()
    print("=========================================")
    print("POSITION STATE STORE OWNERSHIP AUDIT")
    print("=========================================")
    print()

    test_runtime_uses_session_as_read_source_and_store_as_write_mirror()

    print("POSITION STATE STORE OWNERSHIP AUDIT: PASS")


if __name__ == "__main__":
    main()
