import math

import pandas as pd

from config.trading_config import DEFAULT_TRADING_CONFIG, TradingConfig
from models.market_structure import MarketStructure
from services.intelligence.intelligence_models import IndicatorPack
from services.logging_service import LoggingService


class IndicatorBuilder:
    """
    Builds an IndicatorPack from historical market data.

    Responsibilities
    ----------------
    - Calculate deterministic indicators
    - Build deterministic MarketStructure
    - Convert OHLCV history into IndicatorPack
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
            raise ValueError("History may not be empty.")

        close = history["Close"]
        high = history["High"]
        low = history["Low"]

        latest_price = float(close.iloc[-1])
        latest_volume = float(history["Volume"].iloc[-1])

        indicator_pack = IndicatorPack(
            symbol=symbol,
            rsi=self._calculate_rsi(close),
            trend=self._calculate_trend(close),
            volatility=self._calculate_volatility(close),
            momentum=self._calculate_momentum(close),
            volume=latest_volume,
            price=latest_price,
            market_structure=self._build_market_structure(
                history
            ),
        )

        self.logger.info(
            (
                "Indicators ready | "
                "ATR=%.2f "
                "Support=%.2f "
                "Resistance=%.2f"
            ),
            indicator_pack.market_structure.atr,
            indicator_pack.market_structure.support,
            indicator_pack.market_structure.resistance,
        )

        return indicator_pack

    # ---------------------------------------------------------
    # Market Structure
    # ---------------------------------------------------------

    def _build_market_structure(
        self,
        history: pd.DataFrame,
    ) -> MarketStructure:

        atr = self._calculate_atr(history)

        recent = history.tail(20)

        support = float(recent["Low"].min())
        resistance = float(recent["High"].max())

        swing_low = float(history["Low"].tail(10).min())
        swing_high = float(history["High"].tail(10).max())

        average_range = float(
            (history["High"] - history["Low"])
            .tail(20)
            .mean()
        )

        return MarketStructure(
            atr=atr,
            average_range=average_range,
            swing_high=swing_high,
            swing_low=swing_low,
            resistance=resistance,
            support=support,
        )

    def _calculate_atr(
        self,
        history: pd.DataFrame,
        period: int = 14,
    ) -> float:

        high = history["High"]
        low = history["Low"]
        close = history["Close"]

        previous_close = close.shift(1)

        true_range = pd.concat(
            [
                high - low,
                (high - previous_close).abs(),
                (low - previous_close).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = true_range.rolling(period).mean().iloc[-1]

        return float(atr)

    # ---------------------------------------------------------
    # Existing indicators
    # ---------------------------------------------------------

    def _calculate_rsi(
        self,
        close: pd.Series,
    ) -> float:

        period = self.config.rsi_period

        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss.replace(0, 1e-9)

        rsi = 100 - (100 / (1 + rs))

        return max(0.0, min(100.0, float(rsi.iloc[-1])))

    def _calculate_trend(
        self,
        close: pd.Series,
    ) -> float:

        sma = close.rolling(
            self.config.trend_period
        ).mean()

        latest = float(close.iloc[-1])
        average = float(sma.iloc[-1])

        if average == 0:
            return 0.0

        # Express the distance from the moving average as a signed score.
        # The former latest/average ratio was almost always close to +1 and
        # could not represent a downtrend after clamping. A five-percent
        # deviation now maps to the full +/-1 range.
        deviation = (latest - average) / average
        score = deviation / 0.05

        return max(-1.0, min(1.0, score))

    def _calculate_momentum(
        self,
        close: pd.Series,
    ) -> float:

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

    def _calculate_volatility(
        self,
        close: pd.Series,
    ) -> float:

        period = self.config.volatility_period

        returns = close.pct_change()

        volatility = (
            returns
            .rolling(period)
            .std()
            .iloc[-1]
        )

        # Downstream intelligence normalizes percentage values on a 0..100
        # scale. Return annualized realized volatility in percentage points
        # instead of a raw daily decimal (for example 22.0, not 0.014).
        annualized_percent = float(volatility) * math.sqrt(252.0) * 100.0

        return max(0.0, min(100.0, annualized_percent))
