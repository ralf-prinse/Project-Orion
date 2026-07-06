from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndicatorConfig:
    rsi_period: int = 14
    trend_period: int = 20
    momentum_period: int = 10
    volatility_period: int = 20


@dataclass(frozen=True)
class SupportedMarket:
    name: str
    country: str
    currency: str
    exchanges: tuple[str, ...]


@dataclass(frozen=True)
class TradingConfig:
    broker_name: str
    account_currency: str
    default_market_currency: str
    default_universe: str
    supported_markets: tuple[SupportedMarket, ...]
    indicators: IndicatorConfig


TRADING_CONFIG = TradingConfig(
    broker_name="DEGIRO",
    account_currency="EUR",
    default_market_currency="USD",
    default_universe="degiro_us_stocks",
    supported_markets=(
        SupportedMarket(
            name="United States",
            country="US",
            currency="USD",
            exchanges=("NASDAQ", "NYSE"),
        ),
        SupportedMarket(
            name="Euronext Amsterdam",
            country="NL",
            currency="EUR",
            exchanges=("Euronext Amsterdam",),
        ),
        SupportedMarket(
            name="Xetra",
            country="DE",
            currency="EUR",
            exchanges=("Xetra",),
        ),
    ),
    indicators=IndicatorConfig(),
)

DEFAULT_TRADING_CONFIG = TRADING_CONFIG