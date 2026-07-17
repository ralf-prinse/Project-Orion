from pathlib import Path

FILE = Path("services/ibkr/ibkr_order_transport.py")

text = FILE.read_text(encoding="utf-8")

old = """        if (
            self.active_order_id is not None
            and int(reqId) in {-1, self.active_order_id}
        ):
            self.outcome = IbkrOrderOutcome(status="REJECTED", message=message)
            self.terminal_event.set()
"""

new = """        if (
            self.active_order_id is not None
            and int(reqId) in {-1, self.active_order_id}
        ):
            warning_text = str(errorString).lower()

            if (
                error_code == 399
                and "will not be placed at the exchange until" in warning_text
            ):
                logger.warning(
                    "IBKR informational warning preserved: %s",
                    message,
                )
                return

            self.outcome = IbkrOrderOutcome(
                status="REJECTED",
                message=message,
            )
            self.terminal_event.set()
"""

if old not in text:
    raise RuntimeError("Het verwachte codeblok is niet gevonden.")

text = text.replace(old, new, 1)

FILE.write_text(text, encoding="utf-8")

print()
print("✓ IBKR warning 399 patch toegepast.")
print()