import pandas as pd

from config.trading_config import DEFAULT_TRADING_CONFIG, TradingConfig
from services.intelligence.intelligence_models import IndicatorPack
from services.logging_service import LoggingService


class IndicatorBuilder:
    """
    Builds an IndicatorPack from historical market data.

    Responsibilities
    ----------------
    - Calculate deterministic indicators
    - Convert OHLCV history into IndicatorPack
    - Log calculation lifecycle
    """

    def __init__(self, config: TradingConfig | None = None):
        self.config = config or DEFAULT_TRADING_CONFIG.indicators
        self.logger = LoggingService.get_logger("IndicatorBuilder")

    def build(
        self,
        symbol: str,
        history: pd.DataFrame,
    ) -> IndicatorPack:

        self.logger.info(
            "Building indicators for %s",
            symbol,
        )

        if history.empty:
            self.logger.error(
                "No historical data available for %s",
                symbol,
            )
            raise ValueError("History may not be empty.")

        close = history["Close"]

        latest_price = float(close.iloc[-1])

        rsi = self._calculate_rsi(close)
        trend = self._calculate_trend(close)
        momentum = self._calculate_momentum(close)
        volatility = self._calculate_volatility(close)

        latest_volume = float(history["Volume"].iloc[-1])

        indicator_pack = IndicatorPack(
            symbol=symbol,
            rsi=rsi,
            trend=trend,
            volatility=volatility,
            momentum=momentum,
            volume=latest_volume,
            price=latest_price,
        )

        self.logger.info(
            (
                "Indicators ready for %s | "
                "RSI=%.2f Trend=%.3f "
                "Momentum=%.2f Volatility=%.5f"
            ),
            symbol,
            rsi,
            trend,
            momentum,
            volatility,
        )

        return indicator_pack

    def _calculate_rsi(self, close: pd.Series) -> float:
        period = self.config.rsi_period

        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss.replace(0, 1e-9)

        rsi = 100 - (100 / (1 + rs))

        value = float(rsi.iloc[-1])

        return max(0.0, min(100.0, value))

    def _calculate_trend(self, close: pd.Series) -> float:
        period = self.config.trend_period

        sma = close.rolling(period).mean()

        latest = float(close.iloc[-1])
        average = float(sma.iloc[-1])

        if average == 0:
            return 0.5

        score = latest / average

        return max(0.0, min(1.0, score))

    def _calculate_momentum(self, close: pd.Series) -> float:
        period = self.config.momentum_period

        if len(close) <= period:
            return 50.0

        previous = float(close.iloc[-period])
        latest = float(close.iloc[-1])

        if previous == 0:
            return 50.0

        percentage = ((latest - previous) / previous) * 100

        score = 50 + percentage

        return max(0.0, min(100.0, score))

    def _calculate_volatility(self, close: pd.Series) -> float:
        period = self.config.volatility_period

        returns = close.pct_change()

        volatility = (
            returns
            .rolling(period)
            .std()
            .iloc[-1]
        )

        return float(volatility)