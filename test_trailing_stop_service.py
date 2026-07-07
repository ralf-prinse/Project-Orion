from models.position_state import PositionState
from services.risk.trailing_stop_service import TrailingStopService


def run():

    service = TrailingStopService()

    state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=100.0,
        highest_price=110.0,
        current_price=110.0,
        break_even_active=True,
    )

    result = service.evaluate(
        state=state,
        current_price=115.0,
    )

    print(result)

    assert result.activated is True
    assert result.highest_price == 115.0
    assert result.new_stop_loss > 100.0

    print("PASS")


if __name__ == "__main__":
    run()