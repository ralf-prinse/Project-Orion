from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

import exchange_calendars as xcals
import pandas as pd

from models.market_session import (
    MarketDefinition,
    MarketSessionState,
    MarketSessionStatus,
)


class MarketSessionService:
    """
    Determines whether Orion may process a symbol at a given time.

    Initial supported market groups:

    - Euronext Amsterdam
    - German regular market session
    - United States regular market session

    DST is handled by Python's IANA timezone database through zoneinfo.

    Session dates, exchange holidays and special closes are supplied by
    exchange_calendars. Orion fails closed when a calendar cannot resolve
    the requested date.
    """

    AMSTERDAM = MarketDefinition(
        code="XAMS",
        name="Euronext Amsterdam",
        timezone_name="Europe/Amsterdam",
        open_hour=9,
        open_minute=0,
        close_hour=17,
        close_minute=30,
    )

    GERMANY = MarketDefinition(
        code="XETR",
        name="German Market",
        timezone_name="Europe/Berlin",
        open_hour=9,
        open_minute=0,
        close_hour=17,
        close_minute=30,
    )

    UNITED_STATES = MarketDefinition(
        code="XUSA",
        name="United States Market",
        timezone_name="America/New_York",
        open_hour=9,
        open_minute=30,
        close_hour=16,
        close_minute=0,
    )

    MARKETS = (
        AMSTERDAM,
        GERMANY,
        UNITED_STATES,
    )

    CALENDAR_NAMES = {
        "XAMS": "XAMS",
        "XETR": "XETR",
        "XUSA": "XNYS",
    }

    def resolve_market(
        self,
        symbol: str,
    ) -> MarketDefinition:
        normalized = self._normalize_symbol(symbol)

        if normalized.endswith(".AS"):
            return self.AMSTERDAM

        if normalized.endswith(".DE"):
            return self.GERMANY

        # Orion's current universe treats suffixless equity symbols
        # as United States listings. Later this should be replaced by
        # explicit exchange metadata in the universe file.
        return self.UNITED_STATES

    def get_status(
        self,
        market: MarketDefinition,
        now: datetime | None = None,
    ) -> MarketSessionStatus:
        evaluated_at_utc = self._as_utc(
            now or datetime.now(UTC)
        )

        timezone = ZoneInfo(
            market.timezone_name
        )
        local_time = evaluated_at_utc.astimezone(
            timezone
        )

        calendar = self._calendar_for(market)
        session_label = pd.Timestamp(local_time.date())
        is_session = calendar.is_session(session_label)

        session_open = None
        session_close = None

        if is_session:
            session_open = calendar.session_open(
                session_label
            ).to_pydatetime().astimezone(timezone)
            session_close = calendar.session_close(
                session_label
            ).to_pydatetime().astimezone(timezone)

        if (
            is_session
            and session_open
            <= local_time
            < session_close
        ):
            return MarketSessionStatus(
                market=market,
                state=MarketSessionState.OPEN,
                evaluated_at_utc=evaluated_at_utc,
                local_time=local_time,
                session_open=session_open,
                session_close=session_close,
                next_open=session_open,
                reason="Official exchange session is open.",
            )

        next_open = self._calendar_next_open(
            calendar=calendar,
            market=market,
            local_time=local_time,
            session_label=session_label,
            session_open=session_open,
        )

        return MarketSessionStatus(
            market=market,
            state=MarketSessionState.CLOSED,
            evaluated_at_utc=evaluated_at_utc,
            local_time=local_time,
            session_open=session_open,
            session_close=session_close,
            next_open=next_open,
            reason=self._closed_reason(
                local_time=local_time,
                session_open=session_open,
                session_close=session_close,
                is_session=is_session,
            ),
        )

    def get_symbol_status(
        self,
        symbol: str,
        now: datetime | None = None,
    ) -> MarketSessionStatus:
        return self.get_status(
            market=self.resolve_market(symbol),
            now=now,
        )

    def is_symbol_market_open(
        self,
        symbol: str,
        now: datetime | None = None,
    ) -> bool:
        return self.get_symbol_status(
            symbol=symbol,
            now=now,
        ).is_open

    def get_open_symbols(
        self,
        symbols: list[str],
        now: datetime | None = None,
    ) -> list[str]:
        evaluated_at = now or datetime.now(UTC)

        return [
            symbol
            for symbol in symbols
            if self.is_symbol_market_open(
                symbol=symbol,
                now=evaluated_at,
            )
        ]

    def get_market_statuses(
        self,
        now: datetime | None = None,
    ) -> list[MarketSessionStatus]:
        evaluated_at = now or datetime.now(UTC)

        return [
            self.get_status(
                market=market,
                now=evaluated_at,
            )
            for market in self.MARKETS
        ]

    def any_market_open(
        self,
        now: datetime | None = None,
    ) -> bool:
        return any(
            status.is_open
            for status in self.get_market_statuses(
                now=now
            )
        )

    def next_market_open(
        self,
        now: datetime | None = None,
    ) -> datetime:
        statuses = self.get_market_statuses(
            now=now
        )

        open_markets = [
            status
            for status in statuses
            if status.is_open
        ]

        if open_markets:
            return min(
                status.evaluated_at_utc
                for status in open_markets
            )

        return min(
            status.next_open.astimezone(UTC)
            for status in statuses
        )

    def seconds_until_next_market_open(
        self,
        now: datetime | None = None,
    ) -> int:
        evaluated_at_utc = self._as_utc(
            now or datetime.now(UTC)
        )

        if self.any_market_open(
            now=evaluated_at_utc
        ):
            return 0

        next_open = self.next_market_open(
            now=evaluated_at_utc
        )

        return max(
            0,
            int(
                (
                    next_open
                    - evaluated_at_utc
                ).total_seconds()
            ),
        )

    def _closed_reason(
        self,
        local_time: datetime,
        session_open: datetime | None,
        session_close: datetime | None,
        is_session: bool,
    ) -> str:
        if not is_session:
            return "Exchange holiday or non-trading day."

        if session_open is not None and local_time < session_open:
            return "Market has not opened yet."

        if session_close is not None and local_time >= session_close:
            return "Official exchange session has closed."

        return "Market is closed."

    def _calendar_for(self, market: MarketDefinition):
        calendar_name = self.CALENDAR_NAMES.get(market.code)

        if calendar_name is None:
            raise ValueError(
                f"No official exchange calendar configured for {market.code}."
            )

        return xcals.get_calendar(calendar_name)

    def _calendar_next_open(
        self,
        *,
        calendar,
        market: MarketDefinition,
        local_time: datetime,
        session_label,
        session_open: datetime | None,
    ) -> datetime:
        timezone = ZoneInfo(market.timezone_name)

        if session_open is not None and local_time < session_open:
            return session_open

        try:
            next_label = calendar.date_to_session(
                session_label + pd.Timedelta(days=1),
                direction="next",
            )
            return calendar.session_open(
                next_label
            ).to_pydatetime().astimezone(timezone)
        except Exception as exc:
            raise RuntimeError(
                "Official exchange calendar could not resolve the next "
                f"open for {market.code}."
            ) from exc

    def _as_utc(
        self,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            return value.replace(
                tzinfo=UTC
            )

        return value.astimezone(UTC)

    def _normalize_symbol(
        self,
        symbol: str,
    ) -> str:
        normalized = str(symbol).strip().upper()

        if not normalized:
            raise ValueError(
                "Symbol is required."
            )

        return normalized
