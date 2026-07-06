from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from models.trade_lifecycle import Trade


class TradeCard(QFrame):
    """
    Professional visual card for one open trade.

    Presentation only.
    No trading decisions.
    No persistence.
    """

    def __init__(self, theme, trade: Trade):
        super().__init__()

        self.theme = theme
        self.trade = trade

        self.setObjectName("TradeCard")
        self.setStyleSheet(self._style())

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        layout.addWidget(self._header())
        layout.addWidget(self._price_section())
        layout.addWidget(self._risk_plan_section())
        layout.addWidget(self._progress_section())
        layout.addWidget(self._context_section())
        layout.addWidget(self._exit_section())

        self.setLayout(layout)

    def _header(self) -> QWidget:
        widget = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        symbol = QLabel(self.trade.symbol)
        symbol.setStyleSheet(
            """
            QLabel {
                color: #f9fafb;
                font-size: 22px;
                font-weight: bold;
            }
            """
        )

        status = QLabel("🟢 OPEN")
        status.setAlignment(Qt.AlignmentFlag.AlignRight)
        status.setStyleSheet(
            """
            QLabel {
                color: #22c55e;
                font-size: 14px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(symbol, 0, 0)
        layout.addWidget(status, 0, 1)

        widget.setLayout(layout)
        return widget

    def _price_section(self) -> QWidget:
        return self._grid_section(
            title="Prijs & positie",
            rows=[
                ("Aantal", str(self.trade.quantity)),
                ("Entry", self._money(self.trade.entry_price)),
                ("Huidige koers", self._money(self.trade.current_price)),
                (
                    "P/L",
                    (
                        f"{self._pnl_icon()} "
                        f"{self._money(self.trade.unrealized_profit_loss)} "
                        f"({self.trade.unrealized_profit_loss_percent:.2f}%)"
                    ),
                ),
            ],
        )

    def _risk_plan_section(self) -> QWidget:
        target_1 = self.trade.target_1 or self.trade.take_profit

        return self._grid_section(
            title="RiskPlan",
            rows=[
                ("Stop-loss", self._money(self.trade.stop_loss)),
                ("Target 1", self._money(target_1)),
                ("Target 2", self._money(self.trade.target_2)),
                ("Target 3", self._money(self.trade.target_3)),
                ("Risk", f"{self.trade.risk_percent:.2f}%"),
                ("Reward", f"{self.trade.reward_percent:.2f}%"),
                ("R/R", f"{self.trade.risk_reward_ratio:.2f}"),
                ("Confidence", f"{self.trade.risk_plan_confidence * 100:.0f}%"),
            ],
        )

    def _progress_section(self) -> QWidget:
        target_1 = self.trade.target_1 or self.trade.take_profit
        progress = self._progress_to_target(target_1)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        title = QLabel("Progress richting Target 1")
        title.setStyleSheet(self._section_title_style())

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(int(round(progress)))
        progress_bar.setTextVisible(True)
        progress_bar.setFormat(f"{progress:.0f}%")
        progress_bar.setMinimumHeight(18)
        progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #111827;
                border: 1px solid #374151;
                border-radius: 8px;
                color: #f9fafb;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
            }

            QProgressBar::chunk {
                background-color: #22c55e;
                border-radius: 8px;
            }
            """
        )

        layout.addWidget(title)
        layout.addWidget(progress_bar)

        widget.setLayout(layout)
        return widget

    def _context_section(self) -> QWidget:
        return self._grid_section(
            title="Adaptive context",
            rows=self._adaptive_context_rows(),
        )

    def _exit_section(self) -> QWidget:
        widget = QLabel(f"{self._exit_icon()} Exit status: {self.trade.exit_signal.value}")
        widget.setStyleSheet(
            """
            QLabel {
                color: #d1d5db;
                font-size: 14px;
                font-weight: bold;
                padding-top: 6px;
            }
            """
        )
        return widget

    def _grid_section(
        self,
        title: str,
        rows: list[tuple[str, str]],
    ) -> QWidget:
        widget = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet(self._section_title_style())

        layout.addWidget(title_label, 0, 0, 1, 2)

        for index, (label, value) in enumerate(rows, start=1):
            label_widget = QLabel(label)
            label_widget.setStyleSheet(self._label_style())

            value_widget = QLabel(value)
            value_widget.setAlignment(Qt.AlignmentFlag.AlignRight)
            value_widget.setStyleSheet(self._value_style(value))

            layout.addWidget(label_widget, index, 0)
            layout.addWidget(value_widget, index, 1)

        widget.setLayout(layout)
        return widget

    def _adaptive_context_rows(self) -> list[tuple[str, str]]:
        notes = self.trade.risk_plan_notes

        if not notes:
            return [("Context", "Niet beschikbaar")]

        parts: dict[str, str] = {}

        for item in notes.split("|"):
            if "=" not in item:
                continue

            key, value = item.split("=", 1)
            parts[key.strip().lower()] = value.strip().upper()

        rows: list[tuple[str, str]] = []

        if "regime" in parts:
            rows.append(("Regime", self._regime_label(parts["regime"])))

        if "volatility" in parts:
            rows.append(("Volatiliteit", self._volatility_label(parts["volatility"])))

        if "risk" in parts:
            rows.append(("Risk score", parts["risk"]))

        return rows or [("Context", notes)]

    def _progress_to_target(self, target: float) -> float:
        if self.trade.entry_price <= 0:
            return 0.0

        if target <= self.trade.entry_price:
            return 0.0

        progress = (
            (self.trade.current_price - self.trade.entry_price)
            / (target - self.trade.entry_price)
        ) * 100

        return max(0.0, min(100.0, progress))

    def _money(self, value: float) -> str:
        return f"€{value:,.2f}"

    def _pnl_icon(self) -> str:
        if self.trade.unrealized_profit_loss > 0:
            return "🟢"

        if self.trade.unrealized_profit_loss < 0:
            return "🔴"

        return "⚪"

    def _exit_icon(self) -> str:
        value = str(self.trade.exit_signal.value).upper()

        if value == "HOLD_POSITION":
            return "🟢"

        if value in {"TAKE_PROFIT", "TRAILING_STOP"}:
            return "🟡"

        return "🔴"

    def _regime_label(self, regime: str) -> str:
        if regime == "BULL":
            return "Bullish 🟢"

        if regime == "BEAR":
            return "Bearish 🔴"

        if regime == "SIDEWAYS":
            return "Sideways 🟡"

        return regime.title()

    def _volatility_label(self, volatility: str) -> str:
        if volatility == "LOW":
            return "Laag 🟢"

        if volatility in {"NORMAL", "MEDIUM"}:
            return "Normaal 🟡"

        if volatility == "HIGH":
            return "Hoog 🔴"

        return volatility.title()

    def _section_title_style(self) -> str:
        return """
        QLabel {
            color: #f9fafb;
            font-size: 15px;
            font-weight: bold;
            margin-top: 4px;
        }
        """

    def _label_style(self) -> str:
        return """
        QLabel {
            color: #9ca3af;
            font-size: 13px;
        }
        """

    def _value_style(self, value: str) -> str:
        color = "#d1d5db"

        if "🟢" in value:
            color = "#22c55e"

        if "🔴" in value:
            color = "#ef4444"

        if "🟡" in value:
            color = "#f59e0b"

        return f"""
        QLabel {{
            color: {color};
            font-size: 13px;
            font-weight: bold;
        }}
        """

    def _style(self) -> str:
        return """
        QFrame#TradeCard {
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 16px;
            margin-bottom: 14px;
        }
        """