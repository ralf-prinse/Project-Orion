from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class FxRate:
    from_currency: str
    to_currency: str
    rate: float
    source: str


class FxRateService:
    """
    Live foreign exchange rate service.

    Uses Frankfurter.app, based on ECB reference rates.
    """

    DEFAULT_RATES = {
        ("EUR", "USD"): 1.17,
        ("USD", "EUR"): 0.85,
    }

    def __init__(self) -> None:
        self._cache: dict[tuple[str, str], FxRate] = {}

    def get_rate(
        self,
        from_currency: str,
        to_currency: str,
    ) -> FxRate:
        from_currency = from_currency.strip().upper()
        to_currency = to_currency.strip().upper()

        if from_currency == to_currency:
            return FxRate(
                from_currency=from_currency,
                to_currency=to_currency,
                rate=1.0,
                source="identity",
            )

        cache_key = (from_currency, to_currency)
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = requests.get(
                (
                    "https://api.frankfurter.app/latest"
                    f"?from={from_currency}"
                    f"&to={to_currency}"
                ),
                timeout=5,
            )

            response.raise_for_status()
            data = response.json()

            rate = float(data["rates"][to_currency])

            result = FxRate(
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate,
                source="frankfurter.app",
            )
            self._cache[cache_key] = result
            return result

        except Exception:
            rate = self.DEFAULT_RATES.get(
                (from_currency, to_currency),
                1.0,
            )

            return FxRate(
                from_currency=from_currency,
                to_currency=to_currency,
                rate=rate,
                source="fallback",
            )
