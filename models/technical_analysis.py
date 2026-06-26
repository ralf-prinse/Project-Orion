from dataclasses import dataclass


@dataclass
class TechnicalAnalysis:
    rsi: float
    rsi_signal: str

    ema_20: float
    ema_50: float
    trend_signal: str