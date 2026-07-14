from datetime import UTC, datetime

from models.market_session import (
    MarketSessionState,
)
from services.market_session_service import (
    MarketSessionService,
)


def test_market_resolution():
    service = MarketSessionService()

    assert (
        service.resolve_market("ASML.AS").code
        == "XAMS"
    )
    assert (
        service.resolve_market("BAYN.DE").code
        == "XETR"
    )
    assert (
        service.resolve_market("AAPL").code
        == "XUSA"
    )


def test_european_markets_open_during_regular_session():
    service = MarketSessionService()

    # 10:00 in Amsterdam and Berlin during summer.
    now = datetime(
        2026,
        7,
        14,
        8,
        0,
        tzinfo=UTC,
    )

    assert service.get_symbol_status(
        "ASML.AS",
        now=now,
    ).state is MarketSessionState.OPEN

    assert service.get_symbol_status(
        "BAYN.DE",
        now=now,
    ).state is MarketSessionState.OPEN

    assert service.get_symbol_status(
        "AAPL",
        now=now,
    ).state is MarketSessionState.CLOSED


def test_us_market_open_during_regular_session():
    service = MarketSessionService()

    # 10:00 in New York and 16:00 in the Netherlands.
    now = datetime(
        2026,
        7,
        14,
        14,
        0,
        tzinfo=UTC,
    )

    assert service.get_symbol_status(
        "AAPL",
        now=now,
    ).state is MarketSessionState.OPEN

    assert service.get_symbol_status(
        "ASML.AS",
        now=now,
    ).state is MarketSessionState.OPEN


def test_all_markets_closed_after_us_close():
    service = MarketSessionService()

    now = datetime(
        2026,
        7,
        15,
        2,
        0,
        tzinfo=UTC,
    )

    assert service.any_market_open(
        now=now
    ) is False

    assert (
        service.seconds_until_next_market_open(
            now=now
        )
        > 0
    )


def test_weekend_is_closed():
    service = MarketSessionService()

    now = datetime(
        2026,
        7,
        18,
        14,
        0,
        tzinfo=UTC,
    )

    statuses = service.get_market_statuses(
        now=now
    )

    assert all(
        status.state
        is MarketSessionState.CLOSED
        for status in statuses
    )

    assert all(
        status.next_open > status.local_time
        for status in statuses
    )


def test_dst_difference_between_us_and_europe():
    service = MarketSessionService()

    # On 20 March 2026, the US is already on daylight-saving
    # time while Europe is still on standard time.
    #
    # 13:45 UTC = 09:45 in New York and 14:45 in Amsterdam.
    now = datetime(
        2026,
        3,
        20,
        13,
        45,
        tzinfo=UTC,
    )

    assert service.get_symbol_status(
        "AAPL",
        now=now,
    ).state is MarketSessionState.OPEN

    assert service.get_symbol_status(
        "ASML.AS",
        now=now,
    ).state is MarketSessionState.OPEN


def run():
    test_market_resolution()
    test_european_markets_open_during_regular_session()
    test_us_market_open_during_regular_session()
    test_all_markets_closed_after_us_close()
    test_weekend_is_closed()
    test_dst_difference_between_us_and_europe()

    print("MARKET SESSION SERVICE: PASS")


if __name__ == "__main__":
    run()