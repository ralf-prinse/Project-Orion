from services.scanner.scan_pipeline import ScanPipeline


def main():
    symbols = [
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA",
        "AMD",
        "META",
        "GOOGL",
        "AMZN",
        "NFLX",
        "AVGO",
        "ORCL",
        "PLTR",
        "COIN",
        "SHOP",
        "UBER",
        "CRM",
        "INTC",
        "SMCI",
        "MU",
        "PANW",
    ]

    pipeline = ScanPipeline()
    result = pipeline.run(symbols)

    print("\n=== ORION SCAN PIPELINE TEST ===\n")

    print("STATUS")
    print(f"Universe: {result.status.universe_count}")
    print(f"Quotes: {result.status.quotes_count}")
    print(f"Na prijsfilter: {result.status.after_price_filter}")
    print(f"Na volumefilter: {result.status.after_volume_filter}")
    print(f"Na liquiditeitsfilter: {result.status.after_liquidity_filter}")
    print(f"Na relative strength: {result.status.after_relative_strength_filter}")
    print(f"Na momentum: {result.status.after_momentum_filter}")
    print(f"Technische resultaten: {result.status.technical_results_count}")
    print(f"Koopkansen: {result.status.opportunities_count}")

    if result.status.messages:
        print("\nMELDINGEN")
        for message in result.status.messages:
            print(f"- {message}")

    print("\nTOP KANSEN")

    if not result.opportunities:
        print("Geen hoogwaardige koopkansen gevonden.")
        return

    for index, opportunity in enumerate(result.opportunities, start=1):
        print(f"\n{index}. {opportunity.symbol}")
        print(f"Actie: {opportunity.action}")
        print(f"Vertrouwen: {opportunity.confidence:.0f}%")
        print(f"Reden: {opportunity.reason}")


if __name__ == "__main__":
    main()