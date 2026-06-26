import pandas as pd


def calculate_rsi(
    close: pd.Series,
    period: int = 14,
) -> float | None:
    """
    Bereken de laatste RSI-waarde.

    Parameters
    ----------
    close : pd.Series
        Reeks met slotkoersen.

    period : int
        RSI-periode (standaard 14).

    Returns
    -------
    float | None
    """

    if close is None or close.empty:
        return None

    close = close.dropna()

    if len(close) < period + 1:
        return None

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()

    if avg_loss.iloc[-1] == 0:
        return 100.0

    rs = avg_gain.iloc[-1] / avg_loss.iloc[-1]

    rsi = 100 - (100 / (1 + rs))

    return float(rsi)