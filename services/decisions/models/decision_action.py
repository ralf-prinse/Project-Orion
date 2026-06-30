from enum import Enum


class DecisionAction(Enum):
    """
    Mogelijke eindbeslissingen binnen Project Orion.
    """

    BUY = "BUY"
    WATCH = "WATCH"
    HOLD = "HOLD"
    SELL = "SELL"
    SKIP = "SKIP"