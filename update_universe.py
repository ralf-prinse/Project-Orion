from services.universe.universe_downloader import UniverseDownloader


def main():
    downloader = UniverseDownloader()
    result = downloader.update_us_market()

    print("=== ORION UNIVERSE UPDATE ===")
    print(f"Nasdaq symbols: {result['nasdaq']}")
    print(f"US other symbols: {result['us_other']}")
    print(f"US market totaal: {result['us_market']}")
    print("Bestanden bijgewerkt in data/universes/")


if __name__ == "__main__":
    main()