import pandas as pd


def calculate_macd(
    close: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> dict | None:
    """
    Bereken de laatste MACD-waarden.

    Returns:
        {
            "macd": float,
            "signal": float,
            "histogram": float
        }
    """

    if close is None or close.empty:
        return None

    close = close.dropna()

    if len(close) < slow_period + signal_period:
        return None

    ema_fast = close.ewm(span=fast_period, adjust=False).mean()
    ema_slow = close.ewm(span=slow_period, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line

    latest_macd = macd_line.iloc[-1]
    latest_signal = signal_line.iloc[-1]
    latest_histogram = histogram.iloc[-1]

    if (
        pd.isna(latest_macd)
        or pd.isna(latest_signal)
        or pd.isna(latest_histogram)
    ):
        return None

    return {
        "macd": float(latest_macd),
        "signal": float(latest_signal),
        "histogram": float(latest_histogram),
    }