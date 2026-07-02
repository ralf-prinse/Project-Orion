from dataclasses import dataclass, field


@dataclass(frozen=True)
class IndicatorConfig:
    """
    Configuration for deterministic indicator calculations.
    """

    rsi_period: int = 14
    momentum_period: int = 20
    trend_period: int = 50
    volatility_period: int = 20


@dataclass(frozen=True)
class MarketDataConfig:
    """
    Configuration for market data retrieval.
    """

    history_period: str = "6mo"
    history_interval: str = "1d"


@dataclass(frozen=True)
class ScannerConfig:
    """
    Configuration for the default AI market scanner universe.
    """

    default_symbols: list[str] = field(
        default_factory=lambda: [
            "MSFT",
            "NVDA",
            "AAPL",
            "TSLA",
            "AMZN",
        ]
    )

    max_results: int = 10
    minimum_confidence: float = 0.60


@dataclass(frozen=True)
class BacktestConfig:
    """
    Configuration for deterministic backtest simulation.
    """

    fee_rate: float = 0.001
    slippage_rate: float = 0.0005


@dataclass(frozen=True)
class TradingConfig:
    """
    Root configuration object for the Orion AI trading engine.
    """

    indicators: IndicatorConfig = field(default_factory=IndicatorConfig)
    market_data: MarketDataConfig = field(default_factory=MarketDataConfig)
    scanner: ScannerConfig = field(default_factory=ScannerConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)


DEFAULT_TRADING_CONFIG = TradingConfig()