from pathlib import Path


RUNNER_FILE = Path("run_autonomous_ibkr_paper.py")
UNIVERSE_FILE = Path("data/universes/ibkr_euronext_validation.csv")


def main() -> None:
    if not RUNNER_FILE.exists():
        raise FileNotFoundError(
            f"Bestand niet gevonden: {RUNNER_FILE}"
        )

    runner_text = RUNNER_FILE.read_text(encoding="utf-8")

    old = 'watchlist_path="data/universes/ibkr_us_validation.csv"'
    new = 'watchlist_path="data/universes/ibkr_euronext_validation.csv"'

    if old not in runner_text:
        raise RuntimeError(
            "De verwachte IBKR-watchlistconfiguratie is niet gevonden. "
            "Er is niets aangepast."
        )

    euronext_symbols = """\
ASML.AS
ASMI.AS
BESI.AS
INGA.AS
PHIA.AS
"""

    UNIVERSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    UNIVERSE_FILE.write_text(euronext_symbols, encoding="utf-8")

    updated_runner = runner_text.replace(old, new, 1)
    RUNNER_FILE.write_text(updated_runner, encoding="utf-8")

    print()
    print("✓ Euronext-validatie-universe aangemaakt.")
    print("✓ Autonomous IBKR runner gebruikt nu Nederlandse aandelen.")
    print()
    print("Aangemaakte universe:")
    print(UNIVERSE_FILE)
    print()
    print("Aangepast bestand:")
    print(RUNNER_FILE)
    print()


if __name__ == "__main__":
    main()