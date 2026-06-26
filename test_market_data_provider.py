from services.market_data.yahoo_provider import YahooMarketDataProvider


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
    ]

    provider = YahooMarketDataProvider(batch_size=500)
    quotes = provider.get_quotes(symbols)

    print("\n=== ORION MARKET DATA PROVIDER TEST ===\n")

    print("PROVIDER STATS")
    print(f"Provider: {provider.stats.provider_name}")
    print(f"Symbolen gevraagd: {provider.stats.requested_symbols}")
    print(f"Quotes ontvangen: {provider.stats.received_quotes}")
    print(f"Quotes niet gevonden: {provider.stats.missing_quotes}")
    print(f"Duur: {provider.stats.duration_seconds:.2f} seconden")

    print("\nQUOTES")

    if not quotes:
        print("Geen quotes ontvangen.")
        return

    for quote in quotes:
        print(
            f"{quote.symbol}: "
            f"price={quote.price:.2f}, "
            f"volume={quote.volume}, "
            f"change={quote.change_percent}"
        )


if __name__ == "__main__":
    main()