from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BrokerPosition:
    """
    Immutable snapshot of a position reported by an external broker.

    This model represents broker state only. It does not own or contain
    Orion position lifecycle state, risk management or exit logic.
    """

    account_id: str
    symbol: str
    security_type: str
    exchange: str
    currency: str
    quantity: float
    average_cost: float