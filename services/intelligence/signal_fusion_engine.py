from dataclasses import dataclass
from services.intelligence.intelligence_models import IndicatorPack


@dataclass(frozen=True)
class FusedSignal:
    """
    Clean, deterministic output for downstream systems.
    """
    pressure_score: float
    buy_pressure: float
    sell_pressure: float
    strength: float

    trend: float
    momentum: float
    rsi: float
    volatility: float


class SignalFusionEngine:
    """
    Converts raw indicators → structured market pressure model.

    THIS IS NOT A DECISION ENGINE.
    ONLY SIGNAL TRANSFORMATION.
    """

    def build(self, data: IndicatorPack) -> FusedSignal:

        # -------------------------
        # 1. NORMALIZATION
        # -------------------------
        rsi = self._norm(data.rsi)
        trend = self._clamp(data.trend, -1, 1)
        volatility = self._norm(data.volatility)
        momentum = self._norm(data.momentum)

        # -------------------------
        # 2. CORE MARKET PRESSURE
        # -------------------------
        pressure_score = (
            (trend * 0.40) +
            (momentum * 0.25) +
            (rsi * 0.20) +
            ((1 - volatility) * 0.15)
        )

        # -------------------------
        # 3. BUY / SELL PRESSURE MODEL
        # -------------------------
        buy_pressure = (
            max(0.0, trend) * 0.45 +
            momentum * 0.30 +
            rsi * 0.15 +
            (1 - volatility) * 0.10
        )

        sell_pressure = (
            max(0.0, -trend) * 0.50 +
            (1 - momentum) * 0.20 +
            (1 - rsi) * 0.20 +
            volatility * 0.10
        )

        # -------------------------
        # 4. SIGNAL STRENGTH (confidence of movement)
        # -------------------------
        strength = abs(buy_pressure - sell_pressure)

        return FusedSignal(
            pressure_score=pressure_score,
            buy_pressure=buy_pressure,
            sell_pressure=sell_pressure,
            strength=strength,
            trend=trend,
            momentum=momentum,
            rsi=rsi,
            volatility=volatility,
        )

    # -------------------------
    # Helpers
    # -------------------------
    def _norm(self, value: float) -> float:
        return max(0.0, min(value / 100.0, 1.0))

    def _clamp(self, value: float, min_v: float, max_v: float) -> float:
        return max(min_v, min(max_v, value))