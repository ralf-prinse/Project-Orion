from __future__ import annotations

from ibapi.contract import Contract


class IbkrStockContractFactory:
    """Canonical Orion/Yahoo symbol to IBKR stock contract mapping."""

    def build(self, symbol: str) -> Contract:
        normalized = str(symbol).strip().upper()
        if not normalized:
            raise ValueError("IBKR stock symbol must not be empty.")

        contract = Contract()
        contract.secType = "STK"
        contract.exchange = "SMART"

        if normalized.endswith(".AS"):
            contract.symbol = normalized.removesuffix(".AS")
            contract.currency = "EUR"
            contract.primaryExchange = "AEB"
        elif normalized.endswith(".DE"):
            contract.symbol = normalized.removesuffix(".DE")
            contract.currency = "EUR"
            contract.primaryExchange = "IBIS"
        else:
            contract.symbol = normalized
            contract.currency = "USD"

        return contract
