import pandas as pd

from models.technical_analysis import TechnicalAnalysis


class TechnicalEngine:
    """
    Berekent technische indicatoren en levert één TechnicalAnalysis object terug.
    """

    def analyze(self, history: pd.DataFrame) -> TechnicalAnalysis:
        rsi = self.calculate_rsi(history)
        rsi_signal = self.interpret_rsi(rsi)

        ema_20 = self.calculate_ema(history, 20)
        ema_50 = self.calculate_ema(history, 50)
        trend_signal = self.interpret_ema_trend(history)

        return TechnicalAnalysis(
            rsi=rsi,
            rsi_signal=rsi_signal,
            ema_20=ema_20,
            ema_50=ema_50,
            trend_signal=trend_signal,
        )

    def calculate_rsi(self, history: pd.DataFrame, period: int = 14) -> float:
        if history.empty:
            raise ValueError("Historische data mag niet leeg zijn.")

        if "Close" not in history.columns:
            raise ValueError("Historische data moet een 'Close' kolom bevatten.")

        close_prices = history["Close"]

        if len(close_prices) < period + 1:
            raise ValueError(
                f"Niet genoeg data om RSI te berekenen. Minimaal nodig: {period + 1} rijen."
            )

        delta = close_prices.diff()

        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)

        average_gain = gains.rolling(window=period).mean()
        average_loss = losses.rolling(window=period).mean()

        relative_strength = average_gain / average_loss
        rsi = 100 - (100 / (1 + relative_strength))

        return float(rsi.iloc[-1])

    def interpret_rsi(self, rsi: float) -> str:
        if rsi < 30:
            return "oversold"

        if rsi > 70:
            return "overbought"

        return "neutral"

    def calculate_ema(self, history: pd.DataFrame, period: int) -> float:
        if history.empty:
            raise ValueError("Historische data mag niet leeg zijn.")

        if "Close" not in history.columns:
            raise ValueError("Historische data moet een 'Close' kolom bevatten.")

        if len(history) < period:
            raise ValueError(f"Niet genoeg data om EMA {period} te berekenen.")

        ema = history["Close"].ewm(span=period, adjust=False).mean()

        return float(ema.iloc[-1])

    def interpret_ema_trend(self, history: pd.DataFrame) -> str:
        ema_20 = self.calculate_ema(history, 20)
        ema_50 = self.calculate_ema(history, 50)

        if ema_20 > ema_50:
            return "uptrend"

        if ema_20 < ema_50:
            return "downtrend"

        return "neutral"