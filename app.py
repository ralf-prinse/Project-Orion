import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.portfolio_store import PortfolioStore
from models.portfolio import Portfolio
from providers.yahoo_provider import YahooProvider
from services.scanner_service import ScannerService
from services.trade_manager import TradeManager
from services.watchlist_service import WatchlistService


class OrionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Orion")
        self.resize(900, 650)

        self.watchlist_service = WatchlistService()
        self.provider = YahooProvider()
        self.scanner_service = ScannerService(self.provider)
        self.trade_manager = TradeManager()

        self.portfolio_store = PortfolioStore()
        self.portfolio = self.portfolio_store.load()

        self.title_label = QLabel("Project Orion")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; margin: 20px;"
        )

        self.subtitle_label = QLabel("AI Swing Trading Assistant")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet(
            "font-size: 16px; color: #9ca3af; margin-bottom: 20px;"
        )

        self.scan_button = QPushButton("Analyseer markt")
        self.scan_button.clicked.connect(self.scan_market)
        self.scan_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            """
        )

        self.result_label = QLabel("Klik op 'Analyseer markt' om Orion te laten zoeken naar swing trades.")
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet(
            """
            QLabel {
                font-size: 15px;
                color: #e5e7eb;
                padding: 20px;
            }
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(
            """
            QWidget {
                background-color: #111827;
                color: #f9fafb;
            }
            """
        )

        self.setCentralWidget(container)

    def scan_market(self):
        try:
            self.result_label.setText("Orion analyseert de markt...")

            symbols = self.watchlist_service.load_symbols()

            trade_plans = self.scanner_service.scan(
                symbols=symbols,
                portfolio=self.portfolio,
            )

            managed_trades = self.trade_manager.process_trade_plans(trade_plans)

            self.result_label.setText(
                self.format_trade_advice(
                    trade_plans=trade_plans,
                    managed_trades=managed_trades,
                )
            )

        except Exception as error:
            self.result_label.setText(f"Fout tijdens scan: {error}")

    def format_trade_advice(self, trade_plans, managed_trades):
        buy_plans = [
            plan for plan in trade_plans
            if str(plan.action).upper() in ["BUY", "KOPEN"]
        ]
        hold_plans = [
            plan for plan in trade_plans
            if str(plan.action).upper() in ["HOLD", "VASTHOUDEN"]
        ]
        sell_plans = [
            plan for plan in trade_plans
            if str(plan.action).upper() in ["SELL", "VERKOPEN"]
        ]

        action_count = len(buy_plans) + len(hold_plans) + len(sell_plans)

        html = """
        <div style="font-family: Arial;">
            <h1 style="color:#f9fafb;">Project Orion</h1>
            <p style="color:#9ca3af;">Orion zoekt alleen naar korte swing trades van enkele uren tot enkele dagen.</p>
        """

        html += f"""
            <div style="
                background:#1f2937;
                border-radius:12px;
                padding:16px;
                margin:12px 0;
            ">
                <p><b>Gescand:</b> {len(trade_plans)} aandelen</p>
                <p><b>Concrete acties:</b> {action_count}</p>
                <p><b>Open trade-monitoring:</b> {len(managed_trades)}</p>
            </div>
        """

        if action_count == 0:
            html += """
                <div style="
                    background:#1f2937;
                    border-left:6px solid #9ca3af;
                    border-radius:12px;
                    padding:18px;
                    margin-top:18px;
                ">
                    <h1 style="color:#f9fafb;">GEEN ACTIE</h1>
                    <p>Orion ziet op dit moment geen overtuigende korte termijn trade.</p>
                    <p>Wachten is nu beter dan forceren.</p>
                </div>
            </div>
            """
            return html

        html += self._format_action_block(
            title="KOPEN",
            color="#22c55e",
            plans=buy_plans,
            description="Orion ziet hier een mogelijke swing-trade."
        )

        html += self._format_action_block(
            title="VASTHOUDEN",
            color="#3b82f6",
            plans=hold_plans,
            description="Orion ziet nog geen reden om deze positie te sluiten."
        )

        html += self._format_action_block(
            title="VERKOPEN",
            color="#f97316",
            plans=sell_plans,
            description="Orion adviseert deze positie te sluiten."
        )

        html += "</div>"
        return html

    def _format_action_block(self, title, color, plans, description):
        if not plans:
            return ""

        html = f"""
        <div style="
            background:#1f2937;
            border-left:6px solid {color};
            border-radius:12px;
            padding:18px;
            margin-top:18px;
        ">
            <h2 style="color:{color};">{title}</h2>
            <p style="color:#d1d5db;">{description}</p>
        """

        for plan in plans:
            quantity = getattr(plan, "quantity", 0)

            html += f"""
            <div style="
                background:#111827;
                border-radius:10px;
                padding:14px;
                margin-top:12px;
            ">
                <h3 style="color:#f9fafb;">{plan.symbol}</h3>
                <p><b>Aantal:</b> {quantity}</p>
            </div>
            """

        html += "</div>"
        return html


def main():
    app = QApplication(sys.argv)

    window = OrionWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()