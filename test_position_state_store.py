from models.position_state import PositionState
from services.position_state_store import PositionStateStore


def run():

    store = PositionStateStore()

    state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=100.0,
        current_price=100.0,
    )

    store.save(state)

    loaded = store.load("aapl")

    print(loaded)

    assert loaded is not None
    assert loaded.symbol == "AAPL"

    assert len(store.load_all()) == 1

    store.remove("AAPL")

    assert store.load("AAPL") is None
    assert len(store.load_all()) == 0

    print("PASS")


if __name__ == "__main__":
    run()