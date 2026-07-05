from services.market.fx_rate_service import FxRateService


def main():
    service = FxRateService()

    print("\n=========================================")
    print("ORION FX RATE SERVICE TEST")
    print("=========================================\n")

    eur_usd = service.get_rate("EUR", "USD")
    usd_eur = service.get_rate("USD", "EUR")
    eur_eur = service.get_rate("EUR", "EUR")

    results = [
        eur_usd,
        usd_eur,
        eur_eur,
    ]

    for result in results:
        print(
            f"{result.from_currency} -> {result.to_currency}: "
            f"{result.rate:.4f} "
            f"({result.source})"
        )

    assert eur_usd.rate > 0
    assert usd_eur.rate > 0
    assert eur_eur.rate == 1.0
    assert eur_eur.source == "identity"

    print("\nFX RATE SERVICE: PASS ✅\n")


if __name__ == "__main__":
    main()