from datetime import datetime

import pandas as pd
import yfinance as yf

from models.market_data import MarketData
from providers.base_provider import BaseMarketProvider
from services.logging_service import LoggingService


class YahooProvider(BaseMarketProvider):
    """
    Yahoo Finance market data provider.

    Responsibilities
    ----------------
    - Retrieve current market data
    - Retrieve historical OHLCV data
    - Validate symbols
    - Log market data requests
    """

    def __init__(self):
        self.logger = LoggingService.get_logger("YahooProvider")

    def get_current_price(self, symbol: str) -> float:

        self.logger.info(
            "Requesting current price for %s",
            symbol,
        )

        market_data = self.get_market_data(symbol)

        return market_data.current_price

    def get_market_data(self, symbol: str) -> MarketData:

        symbol = self._clean_symbol(symbol)

        self.logger.info(
            "Downloading market data for %s",
            symbol,
        )

        ticker = yf.Ticker(symbol)

        history = ticker.history(period="5d")

        if history.empty:

            self.logger.error(
                "No market data found for %s",
                symbol,
            )

            raise ValueError(
                f"Geen koersdata gevonden voor: {symbol}"
            )

        latest = history.iloc[-1]

        info = ticker.info

        name = info.get("longName") or info.get(
            "shortName"
        ) or symbol

        exchange = info.get(
            "exchange",
            "Onbekend",
        )

        currency = info.get(
            "currency",
            "Onbekend",
        )

        previous_close = info.get(
            "previousClose"
        )

        if previous_close is None and len(history) >= 2:

            previous_close = float(
                history["Close"].iloc[-2]
            )

        self.logger.info(
            "Market data received for %s",
            symbol,
        )

        return MarketData(
            symbol=symbol,
            name=name,
            exchange=exchange,
            currency=currency,
            current_price=float(latest["Close"]),
            open_price=float(latest["Open"]),
            high_price=float(latest["High"]),
            low_price=float(latest["Low"]),
            previous_close=float(previous_close),
            volume=int(latest["Volume"]),
            timestamp=datetime.now(),
        )

    def get_historical_data(
        self,
        symbol: str,
        period: str = "3mo",
        interval: str = "1d",
    ) -> pd.DataFrame:

        symbol = self._clean_symbol(symbol)

        self.logger.info(
            (
                "Downloading history for %s "
                "(period=%s interval=%s)"
            ),
            symbol,
            period,
            interval,
        )

        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period=period,
            interval=interval,
        )

        if history.empty:

            self.logger.error(
                "No historical data found for %s",
                symbol,
            )

            raise ValueError(
                f"Geen historische koersdata gevonden voor: {symbol}"
            )

        self.logger.info(
            "%s candles downloaded for %s",
            len(history),
            symbol,
        )

        return history

    def _clean_symbol(
        self,
        symbol: str,
    ) -> str:

        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError(
                "Symbol mag niet leeg zijn."
            )

        return symbol