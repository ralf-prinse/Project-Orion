from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ScanProgress:
    """
    Immutable progress update emitted by ScanContext and ScanOrchestrator.

    The GUI, CLI or future scheduler may subscribe to these updates without
    owning any scan logic. Percent values are intentionally simple floats so
    presentation layers can decide how to render them.
    """

    stage: str
    message: str = ""
    percent: float = 0.0
    current: int = 0
    total: int = 0
    completed: bool = False
    failed: bool = False


@dataclass
class ScanContext:
    """
    Input context for an end-to-end Orion scan.

    The context contains scan input and orchestration metadata only. It does
    not calculate indicators, generate signals, make decisions or plan trades.
    This keeps the orchestration layer deterministic and free of domain logic.
    """

    symbols: list[str] = field(default_factory=list)
    max_opportunities: int = 3
    configuration: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    continue_on_error: bool = True
    progress_callback: Callable[[ScanProgress], None] | None = None

    def resolved_symbols(self) -> list[str]:
        """
        Return deterministic, cleaned and de-duplicated symbols.

        Input order is preserved. Empty values are ignored. Symbols are
        upper-cased because all market-data and scanner layers expect canonical
        ticker notation.
        """

        resolved: list[str] = []
        seen: set[str] = set()

        for symbol in self.symbols:
            cleaned_symbol = str(symbol).strip().upper()

            if not cleaned_symbol or cleaned_symbol in seen:
                continue

            resolved.append(cleaned_symbol)
            seen.add(cleaned_symbol)

        return resolved

    def emit_progress(
        self,
        stage: str,
        message: str = "",
        percent: float = 0.0,
        current: int = 0,
        total: int = 0,
        completed: bool = False,
        failed: bool = False,
    ) -> None:
        """
        Emit a deterministic progress update when a callback is registered.
        """

        if self.progress_callback is None:
            return

        progress = ScanProgress(
            stage=stage,
            message=message,
            percent=percent,
            current=current,
            total=total,
            completed=completed,
            failed=failed,
        )
        self.progress_callback(progress)
