from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


@dataclass(frozen=True)
class EarningsRiskDecision:
    allowed: bool
    reason: str
    earnings_date: date | None = None
    data_available: bool = False


class EarningsCalendarService:
    """Reads human/auditor supplied earnings dates; never invents dates."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def evaluate(
        self,
        *,
        symbol: str,
        evaluated_on: date,
        blackout_days: int,
    ) -> EarningsRiskDecision:
        events = self._load()
        normalized_symbol = symbol.strip().upper()
        earnings_date = events.get(normalized_symbol)
        if earnings_date is None:
            return EarningsRiskDecision(
                True,
                "No verified earnings date is available; no event block applied.",
                data_available=False,
            )

        days_until = (earnings_date - evaluated_on).days
        if 0 <= days_until <= blackout_days:
            return EarningsRiskDecision(
                False,
                f"Known earnings event is {days_until} day(s) away.",
                earnings_date=earnings_date,
                data_available=True,
            )
        return EarningsRiskDecision(
            True,
            "Known earnings date is outside the configured blackout window.",
            earnings_date=earnings_date,
            data_available=True,
        )

    def _load(self) -> dict[str, date]:
        if not self.path.exists():
            return {}
        events: dict[str, date] = {}
        with self.path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                symbol = str(row.get("symbol", "")).strip().upper()
                value = str(row.get("earnings_date", "")).strip()
                if symbol and value:
                    events[symbol] = datetime.strptime(
                        value,
                        "%Y-%m-%d",
                    ).date()
        return events
