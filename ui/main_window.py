from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)

from providers.yahoo_provider import YahooProvider
from services.portfolio_store import PortfolioStore
from services.scanner_service import ScannerService
from services.trade_manager import TradeManager
from services.universe_manager import UniverseManager


class OrionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Project Orion")
        self.resize(1100, 720)

        self.provider = YahooProvider()
        self.universe_manager = UniverseManager()
        self.scanner_service = ScannerService(
            provider=self.provider,
            universe_manager=self.universe_manager,
            max_workers=8,
        )
        self.trade_manager = TradeManager()

        self.portfolio_store = PortfolioStore()
        self.portfolio = self.portfolio_store.load()
        self.active_universe = "swing"

        self.pages = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.portfolio_page = self.create_portfolio_page()
        self.history_page = self.create_placeholder_page("Historie", "Hier komt straks de trade history.")
        self.settings_page = self.create_placeholder_page("Instellingen", "Hier komen straks risico, budget en universe-instellingen.")

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.portfolio_page)
        self.pages.addWidget(self.history_page)
        self.pages.addWidget(self.settings_page)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_sidebar())
        main_layout.addWidget(self.pages, stretch=1)

        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet(self.stylesheet())

        self.setCentralWidget(container)

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("ORION")
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 20px;")

        subtitle = QLabel("AI Swing Trader")
        subtitle.setStyleSheet("color: #9ca3af; margin-left: 20px; margin-bottom: 30px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        buttons = [
            ("Dashboard", 0),
            ("Portfolio", 1),
            ("Historie", 2),
            ("Instellingen", 3),
        ]

        for text, index in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda checked=False, i=index: self.pages.setCurrentIndex(i))
            button.setStyleSheet(self.sidebar_button_style())
            layout.addWidget(button)

        sidebar.setLayout(layout)
        sidebar.setStyleSheet("background-color: #0b1120;")
        return sidebar

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        header = QLabel("Goedemorgen Ralf.")
        header.setStyleSheet("font-size: 32px; font-weight: bold; margin-top: 25px;")

        intro = QLabel("Laat Orion de markt analyseren en alleen concrete swing-trade acties tonen.")
        intro.setStyleSheet("font-size: 16px; color: #9ca3af; margin-bottom: 20px;")

        self.scan_button = QPushButton("Analyseer markt")
        self.scan_button.clicked.connect(self.scan_market)
        self.scan_button.setStyleSheet(self.primary_button_style())

        self.advice_label = QLabel("Nog geen analyse uitgevoerd.")
        self.advice_label.setAlignment(Qt.AlignTop)
        self.advice_label.setWordWrap(True)
        self.advice_label.setStyleSheet("font-size: 16px; color: #e5e7eb; padding: 20px;")

        layout.addWidget(header)
        layout.addWidget(intro)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.advice_label)

        page.setLayout(layout)
        return page

    def create_portfolio_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Portfolio")
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-top: 25px;")

        self.portfolio_label = QLabel(self.format_portfolio())
        self.portfolio_label.setWordWrap(True)
        self.portfolio_label.setStyleSheet("font-size: 16px; color: #e5e7eb; padding: 20px;")

        layout.addWidget(title)
        layout.addWidget(self.portfolio_label)

        page.setLayout(layout)
        return page

    def create_placeholder_page(self, title_text, body_text):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel(title_text)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-top: 25px;")

        body = QLabel(body_text)
        body.setStyleSheet("font-size: 16px; color: #9ca3af; padding: 20px;")

        layout.addWidget(title)
        layout.addWidget(body)

        page.setLayout(layout)
        return page

    def scan_market(self):
        try:
            self.advice_label.setText("Orion analyseert de markt...")

            trade_plans = self.scanner_service.scan(
                symbols=None,
                portfolio=self.portfolio,
                universe_name=self.active_universe,
            )

            managed_trades = self.trade_manager.process_trade_plans(
                trade_plans=trade_plans,
                portfolio=self.portfolio,
                execute=False,
            )

            self.advice_label.setText(
                self.format_advice(
                    trade_plans=trade_plans,
                    managed_trades=managed_trades,
                )
            )

            self.portfolio_label.setText(self.format_portfolio())

        except Exception as error:
            self.advice_label.setText(f"Fout tijdens scan: {error}")

    def format_advice(self, trade_plans, managed_trades):
        buy_plans = [p for p in trade_plans if str(p.action).upper() == "BUY"]
        hold_plans = [p for p in trade_plans if str(p.action).upper() == "HOLD"]
        sell_plans = [p for p in trade_plans if str(p.action).upper() == "SELL"]

        action_count = len(buy_plans) + len(hold_plans) + len(sell_plans)

        if action_count == 0:
            return """
            <div style="background:#1f2937; border-radius:16px; padding:24px;">
                <h1 style="color:#f9fafb;">GEEN ACTIE</h1>
                <p>Ik heb de markt geanalyseerd.</p>
                <p>Op dit moment zie ik geen swing-trade die sterk genoeg is.</p>
                <p>Mijn advies: wacht af.</p>
            </div>
            """

        html = """
        <div style="background:#1f2937; border-radius:16px; padding:24px;">
            <h2 style="color:#f9fafb;">Mijn handelsadvies</h2>
        """

        html += self.format_action_cards("KOPEN", "#22c55e", buy_plans)
        html += self.format_action_cards("VASTHOUDEN", "#3b82f6", hold_plans)
        html += self.format_action_cards("VERKOPEN", "#f97316", sell_plans)

        html += "</div>"
        return html

    def format_action_cards(self, title, color, plans):
        if not plans:
            return ""

        html = f"<h2 style='color:{color};'>{title}</h2>"

        for plan in plans:
            html += f"""
            <div style="background:#111827; border-left:5px solid {color}; border-radius:12px; padding:16px; margin:12px 0;">
                <h3 style="color:#f9fafb;">{plan.symbol}</h3>
                <p>Aantal: <b>{plan.quantity}</b></p>
            </div>
            """

        return html

    def format_portfolio(self):
        html = f"""
        <div style="background:#1f2937; border-radius:16px; padding:24px;">
            <h2>Overzicht</h2>
            <p><b>Cash:</b> {self.portfolio.currency} {self.portfolio.cash:.2f}</p>
            <p><b>Open posities:</b> {len(self.portfolio.positions)}</p>
        """

        if not self.portfolio.positions:
            html += "<p>Je hebt momenteel geen open posities.</p></div>"
            return html

        html += "<h2>Posities</h2>"

        for symbol, position in self.portfolio.positions.items():
            quantity = getattr(position, "quantity", 0)
            average_price = getattr(position, "average_price", 0.0)

            html += f"""
            <div style="background:#111827; border-radius:12px; padding:14px; margin:10px 0;">
                <h3>{symbol}</h3>
                <p>Aantal: {quantity}</p>
                <p>Gemiddelde aankoopprijs: {average_price:.2f}</p>
            </div>
            """

        html += "</div>"
        return html

    def stylesheet(self):
        return """
        QWidget {
            background-color: #111827;
            color: #f9fafb;
            font-family: Arial;
        }
        QLabel {
            color: #f9fafb;
        }
        """

    def primary_button_style(self):
        return """
        QPushButton {
            background-color: #2563eb;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        """

    def sidebar_button_style(self):
        return """
        QPushButton {
            text-align: left;
            background-color: transparent;
            color: #d1d5db;
            font-size: 15px;
            padding: 12px 20px;
            border: none;
        }
        QPushButton:hover {
            background-color: #1f2937;
            color: white;
        }
        """