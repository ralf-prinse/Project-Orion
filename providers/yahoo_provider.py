from __future__ import annotations

from datetime import UTC, datetime

import pandas as pd
import yfinance as yf

from models.market_data import MarketData
from providers.base_provider import BaseMarketProvider
from providers.provider_retry_policy import ProviderRetryPolicy
from providers.provider_statistics import ProviderStatistics
from services.logging_service import LoggingService
from services.quote_validation_service import (
    QuoteValidationService,
)


class YahooProvider(BaseMarketProvider):
    """
    Yahoo Finance market-data provider.

    Every price is validated before it may enter Orion.
    Invalid values such as NaN, infinity, zero or negative prices
    raise a clear ValueError and are never returned to the engine.
    """

    def __init__(
        self,
        retry_policy: ProviderRetryPolicy | None = None,
        statistics: ProviderStatistics | None = None,
        quote_validation_service: (
            QuoteValidationService | None
        ) = None,
    ):
        self.logger = LoggingService.get_logger(
            "YahooProvider"
        )
        self.retry_policy = (
            retry_policy
            or ProviderRetryPolicy()
        )
        self.statistics = (
            statistics
            or ProviderStatistics()
        )
        self.quote_validation_service = (
            quote_validation_service
            or QuoteValidationService()
        )

    def get_current_price(
        self,
        symbol: str,
    ) -> float:
        self.logger.info(
            "Requesting current price for %s",
            symbol,
        )

        market_data = self.get_market_data(
            symbol
        )

        return (
            self.quote_validation_service
            .require_valid_price(
                symbol=market_data.symbol,
                value=market_data.current_price,
            )
        )

    def get_market_data(
        self,
        symbol: str,
    ) -> MarketData:
        cleaned_symbol = self._clean_symbol(
            symbol
        )

        return self.retry_policy.run(
            lambda: self._get_market_data_once(
                cleaned_symbol
            ),
            statistics=self.statistics,
        )

    def _get_market_data_once(
        self,
        symbol: str,
    ) -> MarketData:
        self.logger.info(
            "Downloading market data for %s",
            symbol,
        )

        ticker = yf.Ticker(symbol)
        history = ticker.history(
            period="5d"
        )

        if history.empty:
            self.logger.error(
                "No market data found for %s",
                symbol,
            )

            raise ValueError(
                "Geen koersdata gevonden voor: "
                f"{symbol}"
            )

        latest = history.iloc[-1]
        info = ticker.info

        name = (
            info.get("longName")
            or info.get("shortName")
            or symbol
        )

        exchange = info.get(
            "exchange",
            "Onbekend",
        )
        currency = info.get(
            "currency",
            "Onbekend",
        )

        current_price = self._require_price(
            symbol=symbol,
            field_name="Close",
            value=latest.get("Close"),
        )
        open_price = self._require_price(
            symbol=symbol,
            field_name="Open",
            value=latest.get("Open"),
        )
        high_price = self._require_price(
            symbol=symbol,
            field_name="High",
            value=latest.get("High"),
        )
        low_price = self._require_price(
            symbol=symbol,
            field_name="Low",
            value=latest.get("Low"),
        )

        previous_close_value = info.get(
            "previousClose"
        )

        if (
            previous_close_value is None
            and len(history) >= 2
        ):
            previous_close_value = (
                history["Close"].iloc[-2]
            )

        previous_close = self._require_price(
            symbol=symbol,
            field_name="previousClose",
            value=previous_close_value,
        )

        volume = self._normalize_volume(
            symbol=symbol,
            value=latest.get("Volume"),
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
            current_price=current_price,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            previous_close=previous_close,
            volume=volume,
            timestamp=datetime.now(UTC),
        )

    def get_historical_data(
        self,
        symbol: str,
        period: str = "3mo",
        interval: str = "1d",
    ) -> pd.DataFrame:
        cleaned_symbol = self._clean_symbol(
            symbol
        )

        return self.retry_policy.run(
            lambda: self._get_historical_data_once(
                symbol=cleaned_symbol,
                period=period,
                interval=interval,
            ),
            statistics=self.statistics,
        )

    def _get_historical_data_once(
        self,
        symbol: str,
        period: str,
        interval: str,
    ) -> pd.DataFrame:
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
                "Geen historische koersdata "
                f"gevonden voor: {symbol}"
            )

        self.logger.info(
            "%s candles downloaded for %s",
            len(history),
            symbol,
        )

        return history

    def _require_price(
        self,
        *,
        symbol: str,
        field_name: str,
        value: object,
    ) -> float:
        try:
            return (
                self.quote_validation_service
                .require_valid_price(
                    symbol=symbol,
                    value=value,
                )
            )

        except ValueError as error:
            self.logger.warning(
                (
                    "Invalid Yahoo quote for %s "
                    "field=%s value=%r: %s"
                ),
                symbol,
                field_name,
                value,
                error,
            )

            raise ValueError(
                "Invalid Yahoo market data for "
                f"{symbol}, field {field_name}: "
                f"{value!r}"
            ) from error

    def _normalize_volume(
        self,
        *,
        symbol: str,
        value: object,
    ) -> int:
        if value is None:
            self.logger.warning(
                "Missing volume for %s; using 0.",
                symbol,
            )
            return 0

        try:
            volume = float(value)

        except (TypeError, ValueError, OverflowError):
            self.logger.warning(
                (
                    "Invalid volume for %s: %r; "
                    "using 0."
                ),
                symbol,
                value,
            )
            return 0

        if not pd.notna(volume) or volume < 0:
            self.logger.warning(
                (
                    "Non-finite or negative volume "
                    "for %s: %r; using 0."
                ),
                symbol,
                value,
            )
            return 0

        return int(volume)

    def _clean_symbol(
        self,
        symbol: str,
    ) -> str:
        cleaned_symbol = str(
            symbol
        ).strip().upper()

        if not cleaned_symbol:
            raise ValueError(
                "Symbol mag niet leeg zijn."
            )

        return cleaned_symbol