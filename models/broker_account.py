from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BrokerAccount:
    broker_name: str
    account_id: str
    cash: float
    buying_power: float
    currency: str = "EUR"
    status: str = "ACTIVE"