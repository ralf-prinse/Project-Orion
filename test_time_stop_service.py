from models.position_state import PositionState
from services.risk.time_stop_service import TimeStopService


def run():

    service = TimeStopService()

    state = PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=100.0,
        highest_price=112.0,
        current_price=110.0,
        break_even_active=True,
        trailing_stop_active=True,
        target_1_hit=True,
        target_2_hit=False,
        target_3_hit=False,
    )

    print("========== BEFORE LIMIT ==========")

    result = service.evaluate(
        state=state,
        days_open=5,
    )

    print(result)

    assert result.activated is False

    print("PASS")

    print()

    print("========== AFTER LIMIT ==========")

    result = service.evaluate(
        state=state,
        days_open=12,
    )

    print(result)

    assert result.activated is True

    print("PASS")


if __name__ == "__main__":
    run()