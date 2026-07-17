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


def test_nyse_independence_day_observed_is_closed():
    service = MarketSessionService()
    status = service.get_symbol_status(
        "AAPL",
        now=datetime(2026, 7, 3, 16, 0, tzinfo=UTC),
    )

    assert status.is_open is False
    assert "holiday" in status.reason.lower()


def test_nyse_thanksgiving_friday_uses_early_close():
    service = MarketSessionService()
    before_close = service.get_symbol_status(
        "AAPL",
        now=datetime(2026, 11, 27, 17, 59, tzinfo=UTC),
    )
    after_close = service.get_symbol_status(
        "AAPL",
        now=datetime(2026, 11, 27, 18, 1, tzinfo=UTC),
    )

    assert before_close.is_open is True
    assert before_close.session_close.hour == 13
    assert after_close.is_open is False


def test_euronext_good_friday_is_closed():
    service = MarketSessionService()
    status = service.get_symbol_status(
        "ASML.AS",
        now=datetime(2026, 4, 3, 10, 0, tzinfo=UTC),
    )

    assert status.is_open is False
    assert "holiday" in status.reason.lower()


def test_euronext_christmas_eve_uses_early_close():
    service = MarketSessionService()
    before_close = service.get_symbol_status(
        "ASML.AS",
        now=datetime(2026, 12, 24, 13, 0, tzinfo=UTC),
    )
    after_close = service.get_symbol_status(
        "ASML.AS",
        now=datetime(2026, 12, 24, 13, 10, tzinfo=UTC),
    )

    assert before_close.is_open is True
    assert before_close.session_close.hour == 14
    assert before_close.session_close.minute == 5
    assert after_close.is_open is False


def run():
    test_market_resolution()
    test_european_markets_open_during_regular_session()
    test_us_market_open_during_regular_session()
    test_all_markets_closed_after_us_close()
    test_weekend_is_closed()
    test_dst_difference_between_us_and_europe()
    test_nyse_independence_day_observed_is_closed()
    test_nyse_thanksgiving_friday_uses_early_close()
    test_euronext_good_friday_is_closed()
    test_euronext_christmas_eve_uses_early_close()

    print("MARKET SESSION SERVICE: PASS")


if __name__ == "__main__":
    run()
