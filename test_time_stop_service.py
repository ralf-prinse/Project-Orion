from datetime import UTC, datetime, timedelta

from models.position_state import PositionState
from services.risk.time_stop_service import TimeStopService


def build_state(
    opened_at: datetime,
) -> PositionState:
    return PositionState(
        symbol="AAPL",
        entry_price=100.0,
        current_stop_loss=95.0,
        highest_price=105.0,
        current_price=103.0,
        opened_at=opened_at,
    )


def test_time_stop_holds_before_48_hours():
    service = TimeStopService()
    opened_at = datetime(
        2026,
        7,
        10,
        9,
        0,
        tzinfo=UTC,
    )

    result = service.evaluate(
        state=build_state(opened_at),
        maximum_days=2,
        now=opened_at + timedelta(
            hours=47,
            minutes=59,
        ),
    )

    assert result.activated is False
    assert result.maximum_hours == 48.0
    assert result.elapsed_hours < 48.0
    assert result.reason == "Holding period still valid."


def test_time_stop_activates_at_exactly_48_hours():
    service = TimeStopService()
    opened_at = datetime(
        2026,
        7,
        10,
        9,
        0,
        tzinfo=UTC,
    )

    result = service.evaluate(
        state=build_state(opened_at),
        maximum_days=2,
        now=opened_at + timedelta(hours=48),
    )

    assert result.activated is True
    assert result.elapsed_hours == 48.0
    assert result.maximum_hours == 48.0
    assert result.reason == "Maximum holding period reached."


def test_time_stop_accepts_legacy_naive_timestamp():
    service = TimeStopService()
    opened_at = datetime(
        2026,
        7,
        10,
        9,
        0,
    )

    result = service.evaluate(
        state=build_state(opened_at),
        maximum_days=2,
        now=opened_at + timedelta(hours=49),
    )

    assert result.activated is True


def test_time_stop_rejects_invalid_maximum_days():
    service = TimeStopService()
    state = build_state(datetime.now(UTC))

    try:
        service.evaluate(
            state=state,
            maximum_days=0,
        )
    except ValueError as error:
        assert (
            str(error)
            == "maximum_days must be at least 1."
        )
    else:
        raise AssertionError(
            "Expected ValueError for invalid maximum_days."
        )


def run():
    test_time_stop_holds_before_48_hours()
    test_time_stop_activates_at_exactly_48_hours()
    test_time_stop_accepts_legacy_naive_timestamp()
    test_time_stop_rejects_invalid_maximum_days()

    print("TIME STOP SERVICE: PASS")


if __name__ == "__main__":
    run()