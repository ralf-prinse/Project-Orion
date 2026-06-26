import pandas as pd


def calculate_atr(
    candles: pd.DataFrame,
    period: int = 14,
) -> float | None:
    """
    Bereken de laatste Average True Range waarde.
    """

    if candles is None or candles.empty:
        return None

    required_columns = {"High", "Low", "Close"}

    if not required_columns.issubset(set(candles.columns)):
        return None

    high = candles["High"].dropna()
    low = candles["Low"].dropna()
    close = candles["Close"].dropna()

    if len(close) < period + 1:
        return None

    previous_close = close.shift(1)

    high_low = high - low
    high_previous_close = (high - previous_close).abs()
    low_previous_close = (low - previous_close).abs()

    true_range = pd.concat(
        [
            high_low,
            high_previous_close,
            low_previous_close,
        ],
        axis=1,
    ).max(axis=1)

    atr = true_range.ewm(alpha=1 / period, adjust=False).mean()

    latest_atr = atr.iloc[-1]

    if pd.isna(latest_atr):
        return None

    return float(latest_atr)


def calculate_bollinger_bands(
    close: pd.Series,
    period: int = 20,
    standard_deviations: float = 2.0,
) -> dict | None:
    """
    Bereken de laatste Bollinger Bands waarden.

    Returns:
        {
            "middle": float,
            "upper": float,
            "lower": float,
            "width": float
        }
    """

    if close is None or close.empty:
        return None

    close = close.dropna()

    if len(close) < period:
        return None

    middle = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()

    latest_middle = middle.iloc[-1]
    latest_std = std.iloc[-1]

    if pd.isna(latest_middle) or pd.isna(latest_std):
        return None

    upper = latest_middle + (standard_deviations * latest_std)
    lower = latest_middle - (standard_deviations * latest_std)

    if latest_middle == 0:
        width = None
    else:
        width = ((upper - lower) / latest_middle) * 100

    return {
        "middle": float(latest_middle),
        "upper": float(upper),
        "lower": float(lower),
        "width": None if width is None else float(width),
    }