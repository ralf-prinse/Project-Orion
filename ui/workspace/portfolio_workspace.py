from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.workspace.base_workspace import BaseWorkspace


class PortfolioWorkspace(BaseWorkspace):
    """
    Simplified Portfolio workspace.

    One responsibility:
    let the user define the available trading capital Orion may use
    for position-sizing calculations.

    Presentation only.
    No persistence.
    No trading decisions.
    No BUY / HOLD / SELL logic.
    """

    capital_saved = Signal(float)

    def __init__(
        self,
        theme,
        initial_cash: float = 300.00,
        currency: str = "EUR",
    ):
        super().__init__(
            theme=theme,
            title="Portfolio",
            intro=(
                "Stel hier het beschikbare handelskapitaal in dat Orion mag "
                "gebruiken voor positieberekeningen."
            ),
        )

        self.currency = currency

        self.capital_input = QLineEdit()
        self.capital_input.setText(f"{float(initial_cash):.2f}")
        self.capital_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.capital_input.setPlaceholderText("Bijvoorbeeld: 300.00")
        self.capital_input.setStyleSheet(self.input_style())

        self.currency_label = QLabel(self.currency)
        self.currency_label.setStyleSheet(self.currency_style())

        self.save_button = QPushButton("Opslaan")
        self.save_button.setStyleSheet(self.primary_button_style())
        self.save_button.clicked.connect(self._handle_save_clicked)

        self.status_label = QLabel("Trading capital klaar om gebruikt te worden.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(self.status_style("neutral"))

        self._build_layout()

    def set_workspace(self, workspace) -> None:
        """
        Backward-compatible adapter.

        MainWindow may still call set_workspace during startup.
        The simplified Portfolio workspace no longer renders portfolio dashboards.
        """

        return None

    def _build_layout(self) -> None:
        card = QFrame()
        card.setObjectName("TradingCapitalCard")
        card.setStyleSheet(self.card_style())

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(28, 26, 28, 26)
        card_layout.setSpacing(18)

        title = QLabel("Trading Capital")
        title.setStyleSheet(self.card_title_style())

        subtitle = QLabel(
            "Vul het bedrag in dat Orion mag gebruiken voor position sizing."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(self.card_subtitle_style())

        input_row = QWidget()
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(12)

        input_layout.addWidget(self.capital_input, stretch=1)
        input_layout.addWidget(self.currency_label)

        input_row.setLayout(input_layout)

        explanation = QLabel(
            "Orion gebruikt dit bedrag na een Scan Markt om per opportunity "
            "te berekenen hoeveel aandelen binnen je beschikbare budget passen."
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet(self.explanation_style())

        bullets = QLabel(
            "✓ aantal aandelen\n"
            "✓ benodigde investering\n"
            "✓ resterend budget\n"
            "✓ budgetcontrole"
        )
        bullets.setStyleSheet(self.bullet_style())

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(input_row)
        card_layout.addWidget(self.save_button)
        card_layout.addWidget(self.status_label)
        card_layout.addSpacing(8)
        card_layout.addWidget(explanation)
        card_layout.addWidget(bullets)

        card.setLayout(card_layout)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(card)
        container_layout.addStretch(1)
        container.setLayout(container_layout)

        self.add_workspace_widget(container)

    def _handle_save_clicked(self) -> None:
        value_text = self.capital_input.text().strip().replace(",", ".")

        try:
            amount = float(value_text)
        except ValueError:
            self._set_status(
                "Vul een geldig bedrag in, bijvoorbeeld 300.00.",
                "warning",
            )
            return

        if amount <= 0:
            self._set_status(
                "Het beschikbare handelskapitaal moet groter zijn dan 0.",
                "warning",
            )
            return

        self.capital_input.setText(f"{amount:.2f}")
        self.capital_saved.emit(amount)

        self._set_status(
            f"Beschikbaar handelskapitaal opgeslagen: {self.currency} {amount:.2f}.",
            "success",
        )

    def set_capital(self, amount: float, currency: str | None = None) -> None:
        self.capital_input.setText(f"{float(amount):.2f}")

        if currency:
            self.currency = currency
            self.currency_label.setText(currency)

        self._set_status(
            f"Huidig handelskapitaal: {self.currency} {float(amount):.2f}.",
            "neutral",
        )

    def _set_status(self, text: str, status: str) -> None:
        self.status_label.setText(text)
        self.status_label.setStyleSheet(self.status_style(status))

    def card_style(self) -> str:
        return """
        QFrame#TradingCapitalCard {
            background-color: #111827;
            border: 1px solid #374151;
            border-radius: 18px;
        }
        """

    def card_title_style(self) -> str:
        return """
        color: #f9fafb;
        font-size: 22px;
        font-weight: 800;
        """

    def card_subtitle_style(self) -> str:
        return """
        color: #9ca3af;
        font-size: 14px;
        font-weight: 500;
        """

    def input_style(self) -> str:
        return """
        QLineEdit {
            background-color: #020617;
            color: #f9fafb;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 14px 16px;
            font-size: 24px;
            font-weight: 800;
        }

        QLineEdit:focus {
            border: 1px solid #2563eb;
        }
        """

    def currency_style(self) -> str:
        return """
        color: #60a5fa;
        font-size: 20px;
        font-weight: 800;
        min-width: 54px;
        """

    def primary_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: 800;
            padding: 14px 20px;
            border-radius: 12px;
            border: 1px solid #3b82f6;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
            border: 1px solid #60a5fa;
        }

        QPushButton:pressed {
            background-color: #1e40af;
        }
        """

    def status_style(self, status: str) -> str:
        if status == "success":
            color = "#22c55e"
        elif status == "warning":
            color = "#f59e0b"
        else:
            color = "#9ca3af"

        return f"""
        color: {color};
        font-size: 13px;
        font-weight: 600;
        """

    def explanation_style(self) -> str:
        return """
        color: #d1d5db;
        font-size: 14px;
        font-weight: 500;
        line-height: 140%;
        """

    def bullet_style(self) -> str:
        return """
        color: #f9fafb;
        font-size: 14px;
        font-weight: 700;
        line-height: 150%;
        """