from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


@dataclass(frozen=True)
class ScannerPanelRow:
    """
    Presentation-only scanner row.

    Contains already prepared scanner output.
    No trading logic.
    """

    symbol: str
    signal: str
    confidence: str
    reason: str = ""


class ScannerPanel(QWidget):
    """
    Presentation-only live scanner panel.

    Displays scanner opportunities prepared by the controller/presenter.
    Contains no trading logic, no AI logic and no calculations.
    """

    def __init__(self):
        super().__init__()

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(18, 18, 18, 18)
        self._layout.setSpacing(10)

        self.setLayout(self._layout)
        self.setStyleSheet(self._panel_style())

        self.set_empty_state()

    def set_empty_state(self) -> None:
        self._clear()

        title = QLabel("Live Scanner")
        title.setObjectName("ScannerPanelTitle")

        subtitle = QLabel(
            "Nog geen scannerresultaten. Klik op Start Live Scanner."
        )
        subtitle.setObjectName("ScannerPanelSubtitle")
        subtitle.setWordWrap(True)

        self._layout.addWidget(title)
        self._layout.addWidget(subtitle)

    def set_rows(
        self,
        rows: list[ScannerPanelRow],
        status_text: str = "Scanner actief",
    ) -> None:
        self._clear()

        title = QLabel("Live Opportunities")
        title.setObjectName("ScannerPanelTitle")

        status = QLabel(status_text)
        status.setObjectName("ScannerPanelSubtitle")
        status.setWordWrap(True)

        self._layout.addWidget(title)
        self._layout.addWidget(status)

        if not rows:
            empty = QLabel("Geen actieve kansen gevonden.")
            empty.setObjectName("ScannerPanelSubtitle")
            empty.setWordWrap(True)
            self._layout.addWidget(empty)
            return

        for row in rows:
            label = QLabel(self._format_row(row))
            label.setObjectName("ScannerPanelRow")
            label.setWordWrap(True)
            self._layout.addWidget(label)

        self._layout.addStretch(1)

    def _format_row(self, row: ScannerPanelRow) -> str:
        reason = f" — {row.reason}" if row.reason else ""

        return (
            f"{self._signal_icon(row.signal)} "
            f"<b>{row.symbol}</b> &nbsp; "
            f"{row.signal} &nbsp; "
            f"{row.confidence}"
            f"{reason}"
        )

    def _signal_icon(self, signal: str) -> str:
        value = signal.upper()

        if value == "BUY":
            return "🟢"

        if value in ("SELL", "EXIT", "STOP_LOSS"):
            return "🔴"

        if value == "HOLD":
            return "🟡"

        return "⚪"

    def _clear(self) -> None:
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _panel_style(self) -> str:
        return """
        QWidget {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 18px;
        }

        QLabel#ScannerPanelTitle {
            color: #f9fafb;
            font-size: 18px;
            font-weight: 700;
            background: transparent;
            border: none;
        }

        QLabel#ScannerPanelSubtitle {
            color: #9ca3af;
            font-size: 13px;
            background: transparent;
            border: none;
        }

        QLabel#ScannerPanelRow {
            color: #e5e7eb;
            font-size: 14px;
            padding: 8px 10px;
            background-color: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 10px;
        }
        """