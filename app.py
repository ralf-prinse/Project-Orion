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

from models.portfolio import Portfolio
from providers.yahoo_provider import YahooProvider
from services.scanner_service import ScannerService
from services.watchlist_service import WatchlistService


ACTION_LABELS = {
    "BUY": "KOPEN",
    "HOLD": "VASTHOUDEN",
    "SELL": "VERKOPEN",
    "NONE": "GEEN ACTIE",
}


class OrionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Orion")
        self.resize(800, 600)

        self.watchlist_service = WatchlistService()
        self.provider = YahooProvider()
        self.scanner_service = ScannerService(self.provider)

        self.portfolio = Portfolio(
            cash=300.00,
            currency="EUR",
            max_position_percentage=0.35,
        )

        self.title_label = QLabel("Project Orion")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.scan_button = QPushButton("Scan markt")
        self.scan_button.clicked.connect(self.scan_market)

        self.result_label = QLabel("Klik op 'Scan markt' om de watchlist te analyseren.")
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def scan_market(self):
        try:
            self.result_label.setText("Bezig met scannen...")

            symbols = self.watchlist_service.load_symbols()

            trade_plans = self.scanner_service.scan(
                symbols=symbols,
                portfolio=self.portfolio,
            )

            self.result_label.setText(self.format_trade_plans(trade_plans))

        except Exception as error:
            self.result_label.setText(f"Fout tijdens scan: {error}")

        def format_trade_plans(self, trade_plans):
        buy_plans = [plan for plan in trade_plans if plan.action == "BUY"]
        hold_plans = [plan for plan in trade_plans if plan.action == "HOLD"]
        sell_plans = [plan for plan in trade_plans if plan.action == "SELL"]

        action_count = len(buy_plans) + len(hold_plans) + len(sell_plans)

        html = "<h2>Project Orion</h2>"
        html += f"<p><b>Ges Cand:</b> {len(trade_plans)} aandelen</p>"
        html += f"<p><b>Acties gevonden:</b> {action_count}</p>"

        if action_count == 0:
            html += "<h1>GEEN ACTIE</h1>"
            html += "<p>Er zijn op dit moment geen koop-, verkoop- of vasthoudacties.</p>"
            return html

        for title, plans in [
            ("KOPEN", buy_plans),
            ("VASTHOUDEN", hold_plans),
            ("VERKOPEN", sell_plans),
        ]:
            if plans:
                html += f"<h2>{title}</h2>"

                for plan in plans:
                    html += (
                        f"<p><b>{plan.symbol}</b><br>"
                        f"Aantal: {plan.quantity}<br>"
                        f"Geschatte prijs: {plan.estimated_price:.2f}<br>"
                        f"Geschatte waarde: {plan.estimated_value:.2f} {plan.currency}</p>"
                    )

        return html


def main():
    app = QApplication(sys.argv)

    window = OrionWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()