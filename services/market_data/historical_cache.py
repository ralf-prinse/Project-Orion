import json
import re
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path

import pandas as pd


class HistoricalCache:
    """
    Persistente cache voor historische candles.

    Cachelocatie:
    data/cache/historical/

    Per symbool, periode en interval wordt een apart JSON-bestand opgeslagen.
    """

    def __init__(
        self,
        cache_dir: str = "data/cache/historical",
        ttl_hours: int = 24,
    ):
        self.cache_dir = Path(cache_dir)
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> pd.DataFrame | None:
        path = self._path(symbol, period, interval)

        if not path.exists():
            return None

        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)

            cached_at = datetime.fromisoformat(payload["cached_at"])

            if datetime.now() - cached_at > self.ttl:
                return None

            json_data = payload.get("data")

            if not json_data:
                return None

            dataframe = pd.read_json(StringIO(json_data), orient="split")

            if dataframe.empty:
                return None

            return dataframe

        except Exception:
            return None

    def set(
        self,
        symbol: str,
        period: str,
        interval: str,
        data: pd.DataFrame,
    ) -> None:
        if data is None or data.empty:
            return

        path = self._path(symbol, period, interval)

        payload = {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "cached_at": datetime.now().isoformat(),
            "data": data.to_json(orient="split", date_format="iso"),
        }

        with path.open("w", encoding="utf-8") as file:
            json.dump(payload, file)

    def _path(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> Path:
        safe_symbol = self._safe_filename(symbol)
        safe_period = self._safe_filename(period)
        safe_interval = self._safe_filename(interval)

        filename = f"{safe_symbol}_{safe_period}_{safe_interval}.json"

        return self.cache_dir / filename

    def _safe_filename(self, value: str) -> str:
        value = value.upper().strip()
        value = re.sub(r"[^A-Z0-9_-]+", "_", value)

        return value
