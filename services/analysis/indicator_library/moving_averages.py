import pandas as pd


def calculate_sma(
    close: pd.Series,
    period: int,
) -> float | None:
    """
    Bereken de laatste Simple Moving Average waarde.
    """

    if close is None or close.empty:
        return None

    close = close.dropna()

    if len(close) < period:
        return None

    sma = close.rolling(window=period).mean()

    latest_value = sma.iloc[-1]

    if pd.isna(latest_value):
        return None

    return float(latest_value)


def calculate_ema(
    close: pd.Series,
    period: int,
) -> float | None:
    """
    Bereken de laatste Exponential Moving Average waarde.
    """

    if close is None or close.empty:
        return None

    close = close.dropna()

    if len(close) < period:
        return None

    ema = close.ewm(span=period, adjust=False).mean()

    latest_value = ema.iloc[-1]

    if pd.isna(latest_value):
        return None

    return float(latest_value)