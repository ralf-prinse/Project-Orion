from datetime import datetime

from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from models.trade_lifecycle import Trade
from ui.foundation.position_monitor_presenter import PositionMonitorViewModel
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class PositionMonitorWorkspace(BaseWorkspace):
    """
    Position Monitor workspace.

    Presentation only.
    User input is forwarded to the controller.
    """

    def __init__(self, theme, on_monitor_requested):
        super().__init__(
            theme=theme,
            title="Position Monitor",
            intro=(
                "Controleer een open positie en bepaal deterministisch "
                "of Orion vasthouden of verkopen adviseert."
            ),
        )

        self.on_monitor_requested = on_monitor_requested

        self.symbol_input = self._input("AAPL")
        self.quantity_input = self._input("1")
        self.entry_price_input = self._input("180.00")
        self.current_price_input = self._input("185.00")
        self.stop_loss_input = self._input("170.00")
        self.take_profit_input = self._input("200.00")

        self.monitor_button = QPushButton("Controleer positie")
        self.monitor_button.setStyleSheet(self.primary_button_style())
        self.monitor_button.clicked.connect(self._handle_monitor_clicked)

        self.signal_panel = WorkspacePanel(
            theme=self.theme,
            title="Exit Advies",
            body="Nog geen positie gecontroleerd.",
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
        form_layout.setSpacing(12)

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
            label.setStyleSheet(self.theme.muted_text_style())
            form_layout.addWidget(label, row, 0)
            form_layout.addWidget(widget, row, 1)

        form.setLayout(form_layout)

        self.add_workspace_widget(form)
        self.add_workspace_widget(self.monitor_button)
        self.add_workspace_widget(self.signal_panel)
        self.add_workspace_widget(self.pnl_panel)
        self.add_workspace_widget(self.risk_panel)
        self.add_workspace_widget(self.status_panel)

    def _handle_monitor_clicked(self) -> None:
        try:
            trade = Trade(
                symbol=self.symbol_input.text().strip().upper(),
                quantity=int(self.quantity_input.text().strip()),
                entry_price=float(self.entry_price_input.text().strip().replace(",", ".")),
                entry_datetime=datetime.now(),
                entry_reason="Handmatig ingevoerd in Position Monitor.",
                confidence=0.0,
                current_price=float(self.current_price_input.text().strip().replace(",", ".")),
                highest_price=float(self.current_price_input.text().strip().replace(",", ".")),
                lowest_price=float(self.current_price_input.text().strip().replace(",", ".")),
                stop_loss=float(self.stop_loss_input.text().strip().replace(",", ".")),
                take_profit=float(self.take_profit_input.text().strip().replace(",", ".")),
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

    def set_view_model(self, view_model: PositionMonitorViewModel) -> None:
        self.signal_panel.set_title(view_model.signal)
        self.signal_panel.set_body(view_model.signal_explanation)

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
        field.setStyleSheet(self.input_style())
        return field

    def input_style(self) -> str:
        return """
        QLineEdit {
            background-color: #1f2937;
            color: #f9fafb;
            border: 1px solid #374151;
            border-radius: 10px;
            padding: 12px;
            font-size: 15px;
        }

        QLineEdit:focus {
            border: 1px solid #2563eb;
        }
        """

    def primary_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            padding: 12px 22px;
            border-radius: 10px;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
        }
        """