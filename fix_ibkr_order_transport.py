from __future__ import annotations

from pathlib import Path


FILE_PATH = Path("services/ibkr/ibkr_order_transport.py")


def main() -> None:
    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"Bestand niet gevonden: {FILE_PATH.resolve()}"
        )

    content = FILE_PATH.read_text(encoding="utf-8")

    broken_block = '''                if self._client.terminal_event.wait(float(timeout_seconds)):
                    outcome = self._require_outcome()

                    logger.info(
                        (
                            "IBKR order completed: "
                            "status=%s filled=%s avg_price=%s message=%s"
                        ),
                        outcome.status,
                        outcome.filled_quantity,
                        outcome.average_fill_price,
                        outcome.message,
                )

                return outcome
'''

    corrected_block = '''                if self._client.terminal_event.wait(float(timeout_seconds)):
                    outcome = self._require_outcome()

                    logger.info(
                        (
                            "IBKR order completed: "
                            "status=%s filled=%s avg_price=%s message=%s"
                        ),
                        outcome.status,
                        outcome.filled_quantity,
                        outcome.average_fill_price,
                        outcome.message,
                    )

                    return outcome
'''

    if broken_block not in content:
        raise RuntimeError(
            "Het verwachte foutieve codeblok is niet gevonden. "
            "Er is niets aangepast."
        )

    content = content.replace(
        broken_block,
        corrected_block,
        1,
    )

    FILE_PATH.write_text(content, encoding="utf-8")

    print()
    print("IBKR order transport is gecorrigeerd.")
    print(f"Bestand: {FILE_PATH.resolve()}")
    print()


if __name__ == "__main__":
    main()