from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from ui.components.trade_card import TradeCard
from models.trade_lifecycle import Trade
from ui.foundation.position_monitor_presenter import PositionMonitorViewModel
from ui.foundation.trade_monitor_presenter import TradeMonitorListViewModel
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class PositionMonitorWorkspace(BaseWorkspace):
    """
    Position Monitor workspace.

    Presentation only.
    User input is forwarded to the controller.
    """

    INPUT_HEIGHT = 44
    BUTTON_HEIGHT = 48
    LABEL_WIDTH = 120

    def __init__(
        self,
        theme,
        on_monitor_requested,
        on_close_trade_requested=None,
    ):
        super().__init__(
            theme=theme,
            title="Trade Monitor",
            intro=(
                "Volg de volledige levenscyclus van een open trade. "
                "Orion beoordeelt deterministisch of een positie "
                "vastgehouden of gesloten moet worden."
            ),
        )

        self.on_monitor_requested = on_monitor_requested
        self.on_close_trade_requested = on_close_trade_requested

        self.symbol_input = self._input("AAPL")
        self.quantity_input = self._input("1")
        self.entry_price_input = self._input("180.00")
        self.current_price_input = self._input("185.00")
        self.stop_loss_input = self._input("170.00")
        self.take_profit_input = self._input("200.00")

        self.monitor_button = QPushButton("Controleer trade")
        self.monitor_button.setMinimumHeight(self.BUTTON_HEIGHT)
        self.monitor_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.monitor_button.setStyleSheet(self.primary_button_style())
        self.monitor_button.clicked.connect(self._handle_monitor_clicked)

        self.close_trade_button = QPushButton("Close Trade")
        self.close_trade_button.setMinimumHeight(self.BUTTON_HEIGHT)
        self.close_trade_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_trade_button.setStyleSheet(self.danger_button_style())
        self.close_trade_button.clicked.connect(
            self._handle_close_trade_clicked
        )

        self.open_trades_panel = WorkspacePanel(
            theme=self.theme,
            title="Open Trades",
            body="Open trades worden geladen...",
        )
        self.open_trade_cards_container = QWidget()
        self.open_trade_cards_layout = QVBoxLayout()
        self.open_trade_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.open_trade_cards_layout.setSpacing(12)
        self.open_trade_cards_container.setLayout(self.open_trade_cards_layout)
        self.signal_panel = WorkspacePanel(
            theme=self.theme,
            title="Exit Advies",
            body="Nog geen positie gecontroleerd.",
        )

        self.intelligence_panel = WorkspacePanel(
            theme=self.theme,
            title="Exit Intelligence",
            body="Nog geen exit-intelligence beschikbaar.",
        )

        self.pnl_panel = WorkspacePanel(
            theme=self.theme,
            title="Winst / Verlies",
            body="Nog geen positie gecontroleerd.",
        )

        self.risk_panel = WorkspacePanel(
            theme=self.theme,
            title="Risico & Winstdoel",
            body="Nog geen positie gecontroleerd.",
        )

        self.status_panel = WorkspacePanel(
            theme=self.theme,
            title="Status",
            body="Klaar om een positie te controleren.",
        )

        self._build_layout()

    def _build_layout(self) -> None:
        form = QWidget()
        form_layout = QGridLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setHorizontalSpacing(14)
        form_layout.setVerticalSpacing(12)

        fields = [
            ("Symbool", self.symbol_input),
            ("Aantal", self.quantity_input),
            ("Aankoopprijs", self.entry_price_input),
            ("Huidige koers", self.current_price_input),
            ("Stop-loss", self.stop_loss_input),
            ("Winstdoel", self.take_profit_input),
        ]

        for row, (label_text, widget) in enumerate(fields):
            label = QLabel(label_text)
            label.setMinimumWidth(self.LABEL_WIDTH)
            label.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            )
            label.setStyleSheet(self.theme.muted_text_style())

            form_layout.addWidget(label, row, 0)
            form_layout.addWidget(widget, row, 1)

        form_layout.setColumnStretch(0, 0)
        form_layout.setColumnStretch(1, 1)

        form.setLayout(form_layout)

        self.add_workspace_widget(form)
        self.add_workspace_widget(self.monitor_button)
        self.add_workspace_widget(self.close_trade_button)
        self.add_workspace_widget(self.open_trades_panel)
        self.add_workspace_widget(self.open_trade_cards_container)
        self.add_workspace_widget(self.signal_panel)
        self.add_workspace_widget(self.intelligence_panel)
        self.add_workspace_widget(self.pnl_panel)
        self.add_workspace_widget(self.risk_panel)
        self.add_workspace_widget(self.status_panel)

    def _handle_monitor_clicked(self) -> None:
        try:
            current_price = float(
                self.current_price_input.text().strip().replace(",", ".")
            )

            trade = Trade(
                symbol=self.symbol_input.text().strip().upper(),
                quantity=int(self.quantity_input.text().strip()),
                entry_price=float(
                    self.entry_price_input.text().strip().replace(",", ".")
                ),
                entry_datetime=datetime.now(),
                entry_reason="Handmatig ingevoerd in Position Monitor.",
                confidence=0.0,
                current_price=current_price,
                highest_price=current_price,
                lowest_price=current_price,
                stop_loss=float(
                    self.stop_loss_input.text().strip().replace(",", ".")
                ),
                take_profit=float(
                    self.take_profit_input.text().strip().replace(",", ".")
                ),
            )
        except ValueError:
            self.set_status_text(
                "Controleer de invoer. Gebruik geldige getallen voor aantal en prijzen."
            )
            return

        if not trade.symbol:
            self.set_status_text("Vul eerst een geldig symbool in.")
            return

        self.on_monitor_requested(trade)

    def _handle_close_trade_clicked(self) -> None:
        symbol = self.symbol_input.text().strip().upper()

        if not symbol:
            self.set_status_text("Vul eerst een geldig symbool in.")
            return

        if self.on_close_trade_requested is None:
            self.set_status_text(
                "Close Trade is nog niet gekoppeld aan de controller."
            )
            return

        self.on_close_trade_requested(symbol)

    def set_open_trades_view_model(
    self,
    view_model: TradeMonitorListViewModel,
) -> None:
        self.open_trades_panel.set_title(view_model.title)
        self.open_trades_panel.set_body(view_model.summary)
        self.set_status_text(view_model.status)

    def set_view_model(self, view_model: PositionMonitorViewModel) -> None:
        self.signal_panel.set_title(view_model.signal)
        self.signal_panel.set_body(view_model.signal_explanation)

        self.intelligence_panel.set_body(
            f"Exit Score: {view_model.exit_score}\n\n"
            f"{view_model.exit_score_explanation}\n\n"
            f"{view_model.intelligence_summary}"
        )

        self.pnl_panel.set_body(
            f"{view_model.profit_loss}\n\n"
            f"{view_model.profit_loss_explanation}\n\n"
            f"Marktwaarde: {view_model.market_value}"
        )

        self.risk_panel.set_body(
            f"{view_model.risk_status}\n\n"
            f"{view_model.target_status}\n\n"
            f"{view_model.summary}"
        )

        self.set_status_text(view_model.status)

    def set_status_text(self, text: str) -> None:
        self.status_panel.set_body(text)

    def _input(self, value: str) -> QLineEdit:
        field = QLineEdit()
        field.setText(value)
        field.setMinimumHeight(self.INPUT_HEIGHT)
        field.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        field.setStyleSheet(self.input_style())
        return field

    def input_style(self) -> str:
        return """
        QLineEdit {
            background-color: #1f2937;
            color: #f9fafb;
            border: 1px solid #374151;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 15px;
            font-weight: 500;
            selection-background-color: #2563eb;
            selection-color: #ffffff;
        }

        QLineEdit:hover {
            border: 1px solid #4b5563;
        }

        QLineEdit:focus {
            border: 1px solid #2563eb;
            background-color: #111827;
        }
        """

    def primary_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #2563eb;
            color: #ffffff;
            font-size: 15px;
            font-weight: 800;
            padding: 12px 22px;
            border-radius: 10px;
            border: 1px solid #3b82f6;
            text-align: center;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
            border: 1px solid #60a5fa;
        }

        QPushButton:pressed {
            background-color: #1e40af;
        }
        """

    def danger_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #991b1b;
            color: #ffffff;
            font-size: 15px;
            font-weight: 800;
            padding: 12px 22px;
            border-radius: 10px;
            border: 1px solid #dc2626;
            text-align: center;
        }

        QPushButton:hover {
            background-color: #7f1d1d;
            border: 1px solid #ef4444;
        }

        QPushButton:pressed {
            background-color: #450a0a;
        }
        """