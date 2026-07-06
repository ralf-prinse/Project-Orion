from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

from ui.components.metric_card import MetricCard
from ui.foundation.trading_workspace_presenter import TradingWorkspaceViewModel
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.workspace_panel import WorkspacePanel


class TradingWorkspace(BaseWorkspace):
    """
    Trading decision workspace.

    Presentation only.
    No business logic.
    No pipeline parsing.
    """

    def __init__(
        self,
        theme,
        on_analyze_requested,
        on_open_trade_requested=None,
    ):
        super().__init__(
            theme=theme,
            title="Trading Decision",
            intro="Analyseer één symbool met de AI-ready Orion trading pipeline.",
        )

        self.on_analyze_requested = on_analyze_requested
        self.on_open_trade_requested = on_open_trade_requested

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Bijvoorbeeld: TSLA")
        self.symbol_input.setText("TSLA")
        self.symbol_input.setStyleSheet(self.input_style())

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setStyleSheet(self.primary_button_style())
        self.analyze_button.clicked.connect(self._handle_analyze_clicked)

        self.open_trade_button = QPushButton("Open Trade")
        self.open_trade_button.setStyleSheet(self.secondary_button_style())
        self.open_trade_button.setEnabled(False)
        self.open_trade_button.clicked.connect(self._handle_open_trade_clicked)

        self.decision_card = MetricCard(
            theme=self.theme,
            title="Decision",
            value="-",
            subtitle="Nog geen analyse uitgevoerd.",
        )

        self.confidence_card = MetricCard(
            theme=self.theme,
            title="Confidence",
            value="-",
            subtitle="Wacht op analyse.",
        )

        self.pressure_card = MetricCard(
            theme=self.theme,
            title="Pressure Score",
            value="-",
            subtitle="Wacht op analyse.",
        )

        self.position_card = MetricCard(
            theme=self.theme,
            title="Position Size",
            value="-",
            subtitle="Wacht op analyse.",
        )

        self.risk_card = MetricCard(
            theme=self.theme,
            title="Risk",
            value="-",
            subtitle="Wacht op analyse.",
        )

        self.explanation_panel = WorkspacePanel(
            theme=self.theme,
            title="AI Explanation",
            body="Nog geen uitleg beschikbaar.",
        )

        self.status_panel = WorkspacePanel(
            theme=self.theme,
            title="Status",
            body="Klaar voor analyse.",
        )

        self._build_layout()

    def _build_layout(self):
        input_row = QWidget()
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(12)

        input_layout.addWidget(self.symbol_input, stretch=1)
        input_layout.addWidget(self.analyze_button)
        input_layout.addWidget(self.open_trade_button)

        input_row.setLayout(input_layout)

        top_cards = QWidget()
        top_cards_layout = QHBoxLayout()
        top_cards_layout.setContentsMargins(0, 0, 0, 0)
        top_cards_layout.setSpacing(12)

        top_cards_layout.addWidget(self.decision_card)
        top_cards_layout.addWidget(self.confidence_card)
        top_cards_layout.addWidget(self.pressure_card)

        top_cards.setLayout(top_cards_layout)

        bottom_cards = QWidget()
        bottom_cards_layout = QHBoxLayout()
        bottom_cards_layout.setContentsMargins(0, 0, 0, 0)
        bottom_cards_layout.setSpacing(12)

        bottom_cards_layout.addWidget(self.position_card)
        bottom_cards_layout.addWidget(self.risk_card)

        bottom_cards.setLayout(bottom_cards_layout)

        self.add_workspace_widget(input_row)
        self.add_workspace_widget(top_cards)
        self.add_workspace_widget(bottom_cards)
        self.add_workspace_widget(self.explanation_panel)
        self.add_workspace_widget(self.status_panel)

    def _handle_analyze_clicked(self):
        symbol = self.symbol_input.text().strip().upper()

        if not symbol:
            self.set_status_text("Vul eerst een symbool in.")
            return

        self.open_trade_button.setEnabled(False)
        self.on_analyze_requested(symbol)

    def _handle_open_trade_clicked(self):
        if self.on_open_trade_requested is None:
            self.set_status_text("Open Trade actie is nog niet gekoppeld.")
            return

        self.on_open_trade_requested()

    def set_symbol(self, symbol: str) -> None:
        """
        Set the symbol input from an external workspace action.

        Used by Mission Control when a live opportunity is selected.
        Presentation only: this does not run analysis by itself.
        """

        normalized_symbol = str(symbol).strip().upper()

        if not normalized_symbol:
            self.set_status_text("Geen geldig symbool ontvangen.")
            return

        self.symbol_input.setText(normalized_symbol)
        self.open_trade_button.setEnabled(False)
        self.set_status_text(
            f"Symbool {normalized_symbol} geladen vanuit Mission Control."
        )

    def analyze_current_symbol(self) -> None:
        """
        Trigger the existing analyze flow for the current input symbol.
        """

        self._handle_analyze_clicked()

    def set_view_model(self, view_model: TradingWorkspaceViewModel):
        self.decision_card.set_value(view_model.decision)
        self.decision_card.set_subtitle(view_model.decision_reason)

        self.confidence_card.set_value(view_model.confidence)
        self.confidence_card.set_subtitle(view_model.confidence_subtitle)

        self.pressure_card.set_value(view_model.pressure_score)
        self.pressure_card.set_subtitle(view_model.pressure_subtitle)

        self.position_card.set_value(view_model.position_size)
        self.position_card.set_subtitle(view_model.position_subtitle)

        self.risk_card.set_value(view_model.risk_score)
        self.risk_card.set_subtitle(view_model.risk_subtitle)

        self.explanation_panel.set_body(view_model.explanation)

        self.open_trade_button.setEnabled(
            str(view_model.decision).strip().upper() == "BUY"
        )

        self.set_status_text(view_model.status)

    def set_status_text(self, text: str):
        self.status_panel.set_body(text)

    def input_style(self):
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

    def primary_button_style(self):
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

    def secondary_button_style(self):
        return """
        QPushButton {
            background-color: #374151;
            color: #f9fafb;
            font-size: 15px;
            font-weight: bold;
            padding: 12px 22px;
            border-radius: 10px;
            border: 1px solid #4b5563;
        }

        QPushButton:hover {
            background-color: #4b5563;
        }

        QPushButton:disabled {
            background-color: #1f2937;
            color: #6b7280;
            border: 1px solid #374151;
        }
        """