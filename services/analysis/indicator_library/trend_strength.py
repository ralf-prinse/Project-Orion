import pandas as pd


def calculate_adx(
    candles: pd.DataFrame,
    period: int = 14,
) -> dict | None:
    """
    Bereken ADX, +DI en -DI.

    Returns:
        {
            "adx": float,
            "plus_di": float,
            "minus_di": float
        }
    """

    if candles is None or candles.empty:
        return None

    required_columns = {"High", "Low", "Close"}

    if not required_columns.issubset(set(candles.columns)):
        return None

    high = candles["High"].dropna()
    low = candles["Low"].dropna()
    close = candles["Close"].dropna()

    if len(close) < period * 2:
        return None

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where(
        (up_move > down_move) & (up_move > 0),
        0.0,
    )

    minus_dm = down_move.where(
        (down_move > up_move) & (down_move > 0),
        0.0,
    )

    previous_close = close.shift(1)

    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    atr = true_range.ewm(alpha=1 / period, adjust=False).mean()

    plus_di = 100 * (
        plus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr
    )

    minus_di = 100 * (
        minus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr
    )

    dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di))
    adx = dx.ewm(alpha=1 / period, adjust=False).mean()

    latest_adx = adx.iloc[-1]
    latest_plus_di = plus_di.iloc[-1]
    latest_minus_di = minus_di.iloc[-1]

    if (
        pd.isna(latest_adx)
        or pd.isna(latest_plus_di)
        or pd.isna(latest_minus_di)
    ):
        return None

    return {
        "adx": float(latest_adx),
        "plus_di": float(latest_plus_di),
        "minus_di": float(latest_minus_di),
    }