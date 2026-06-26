import argparse
import time

from services.scanner.scan_pipeline import ScanPipeline
from services.universe.universe_loader import UniverseLoader


DEFAULT_SCAN_LIMIT = 100


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Project Orion - Universe Scan Test"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_SCAN_LIMIT,
        help="Aantal symbolen dat gescand moet worden.",
    )

    parser.add_argument(
        "--technical-limit",
        type=int,
        default=100,
        help="Maximum aantal aandelen dat door technische analyse gaat.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    scan_limit = args.limit
    technical_limit = args.technical_limit

    if scan_limit <= 0:
        raise ValueError("Scanlimiet moet groter zijn dan 0.")

    if technical_limit <= 0:
        raise ValueError("Technical limit moet groter zijn dan 0.")

    total_start_time = time.perf_counter()

    loader = UniverseLoader()
    symbols = loader.load_symbols(limit=scan_limit)

    print("\n=== ORION UNIVERSE SCAN TEST ===\n")
    print(f"Universebestand: {loader.universe_file}")
    print(f"Scanlimiet: {scan_limit}")
    print(f"Technical limit: {technical_limit}")
    print(f"Symbolen geladen: {len(symbols)}")

    pipeline = ScanPipeline(
        technical_candidate_limit=technical_limit,
    )
    result = pipeline.run(symbols)

    total_end_time = time.perf_counter()
    total_duration = total_end_time - total_start_time

    print("\nSTATUS")
    print(f"Universe: {result.status.universe_count}")
    print(f"Quotes: {result.status.quotes_count}")
    print(f"Quotes uit cache: {result.status.quote_cache_hits}")
    print(f"Quotes nieuw opgehaald: {result.status.quote_fresh_downloads}")
    print(f"Quotes niet gevonden: {result.status.quote_missing}")
    print(f"Negative cache hits: {result.status.quote_negative_cache_hits}")

    print("\nMARKET DATA PROVIDER")
    print(f"Provider: {result.status.market_data_provider}")
    print(f"Provider symbolen gevraagd: {result.status.provider_requested_symbols}")
    print(f"Provider quotes ontvangen: {result.status.provider_received_quotes}")
    print(f"Provider quotes niet gevonden: {result.status.provider_missing_quotes}")
    print(f"Provider tijd: {result.status.provider_seconds:.2f} sec")

    print("\nFILTERS")
    print(f"Na prijsfilter: {result.status.after_price_filter}")
    print(f"Na volumefilter: {result.status.after_volume_filter}")
    print(f"Na liquiditeitsfilter: {result.status.after_liquidity_filter}")
    print(f"Na relative strength: {result.status.after_relative_strength_filter}")
    print(f"Na momentum: {result.status.after_momentum_filter}")
    print(f"Technische kandidaten: {result.status.technical_candidates_count}")
    print(f"Technische resultaten: {result.status.technical_results_count}")
    print(f"Koopkansen: {result.status.opportunities_count}")

    print("\nPIPELINE PERFORMANCE")
    print(f"QuoteService: {result.status.quote_seconds:.2f} sec")
    print(f"PriceFilter: {result.status.price_filter_seconds:.4f} sec")
    print(f"VolumeFilter: {result.status.volume_filter_seconds:.4f} sec")
    print(f"LiquidityFilter: {result.status.liquidity_filter_seconds:.4f} sec")
    print(f"RelativeStrengthFilter: {result.status.relative_strength_seconds:.4f} sec")
    print(f"MomentumFilter: {result.status.momentum_seconds:.4f} sec")
    print(f"TechnicalScanner: {result.status.technical_scanner_seconds:.2f} sec")
    print(f"RankingEngine: {result.status.ranking_seconds:.4f} sec")
    print(f"Pipeline totaal: {result.status.total_seconds:.2f} sec")
    print(f"Script totaal: {total_duration:.2f} sec")

    if result.status.messages:
        print("\nMELDINGEN")
        for message in result.status.messages:
            print(f"- {message}")

    print("\nTOP 3 KOOPKANSEN")

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