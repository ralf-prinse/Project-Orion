from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

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

    This first foundation deliberately handles regular weekdays and
    regular session hours. Exchange-specific holidays and early closes
    will be added in the calendar-integration commit.
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

        session_open, session_close = (
            self._session_boundaries(
                market=market,
                local_date=local_time.date(),
            )
        )

        is_weekday = local_time.weekday() < 5

        if (
            is_weekday
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
                reason="Regular trading session is open.",
            )

        return MarketSessionStatus(
            market=market,
            state=MarketSessionState.CLOSED,
            evaluated_at_utc=evaluated_at_utc,
            local_time=local_time,
            session_open=(
                session_open
                if is_weekday
                else None
            ),
            session_close=(
                session_close
                if is_weekday
                else None
            ),
            next_open=self._find_next_open(
                market=market,
                local_time=local_time,
            ),
            reason=self._closed_reason(
                local_time=local_time,
                session_open=session_open,
                session_close=session_close,
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

    def _session_boundaries(
        self,
        market: MarketDefinition,
        local_date: date,
    ) -> tuple[datetime, datetime]:
        timezone = ZoneInfo(
            market.timezone_name
        )

        session_open = datetime.combine(
            local_date,
            time(
                hour=market.open_hour,
                minute=market.open_minute,
            ),
            tzinfo=timezone,
        )

        session_close = datetime.combine(
            local_date,
            time(
                hour=market.close_hour,
                minute=market.close_minute,
            ),
            tzinfo=timezone,
        )

        return session_open, session_close

    def _find_next_open(
        self,
        market: MarketDefinition,
        local_time: datetime,
    ) -> datetime:
        candidate_date = local_time.date()

        session_open, _ = self._session_boundaries(
            market=market,
            local_date=candidate_date,
        )

        if (
            local_time.weekday() < 5
            and local_time < session_open
        ):
            return session_open

        candidate_date += timedelta(days=1)

        while candidate_date.weekday() >= 5:
            candidate_date += timedelta(days=1)

        next_open, _ = self._session_boundaries(
            market=market,
            local_date=candidate_date,
        )

        return next_open

    def _closed_reason(
        self,
        local_time: datetime,
        session_open: datetime,
        session_close: datetime,
    ) -> str:
        if local_time.weekday() >= 5:
            return "Market is closed for the weekend."

        if local_time < session_open:
            return "Market has not opened yet."

        if local_time >= session_close:
            return "Regular trading session has closed."

        return "Market is closed."

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