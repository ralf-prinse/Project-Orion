from pathlib import Path


TARGET = Path("services/ibkr/ibkr_broker.py")


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Bestand niet gevonden: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    old = """\
    def _build_contract(self, order: Order) -> Contract:
        contract = Contract()
        contract.symbol = order.symbol.strip().upper()
        contract.secType = "STK"
        contract.exchange = self.exchange
        contract.currency = self.currency
        return contract
"""

    new = """\
    def _build_contract(self, order: Order) -> Contract:
        raw_symbol = order.symbol.strip().upper()

        contract = Contract()
        contract.secType = "STK"
        contract.exchange = self.exchange

        if raw_symbol.endswith(".AS"):
            contract.symbol = raw_symbol.removesuffix(".AS")
            contract.currency = "EUR"
            contract.primaryExchange = "AEB"
        else:
            contract.symbol = raw_symbol
            contract.currency = self.currency

        return contract
"""

    if old not in text:
        raise RuntimeError(
            "De verwachte _build_contract-methode is niet gevonden. "
            "Er is niets aangepast."
        )

    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")

    print()
    print("✓ IBKR-contractbuilder ondersteunt nu Euronext Amsterdam.")
    print("✓ .AS wordt verwijderd uit het IBKR-symbool.")
    print("✓ Valuta wordt EUR en primaryExchange wordt AEB.")
    print()


if __name__ == "__main__":
    main()