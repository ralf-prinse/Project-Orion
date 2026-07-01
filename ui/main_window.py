from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from providers.yahoo_provider import YahooProvider
from services.portfolio_store import PortfolioStore
from services.scanner_service import ScannerService
from services.trade_history_store import TradeHistoryStore
from services.trade_manager import TradeManager
from services.universe_manager import UniverseManager
from ui.design import ORION_DARK_THEME
from ui.foundation.models import GuiPage
from ui.workspace.dashboard_workspace import DashboardWorkspace
from ui.workspace.history_workspace import HistoryWorkspace
from ui.workspace.portfolio_workspace import PortfolioWorkspace
from ui.workspace.scanner_workspace import ScannerWorkspace
from ui.workspace.settings_workspace import SettingsWorkspace
from ui.workspace.workspace_controller import WorkspaceController


class OrionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.theme = ORION_DARK_THEME

        self.setWindowTitle("Project Orion")
        self.resize(
            self.theme.metrics.default_window_width,
            self.theme.metrics.default_window_height,
        )

        self.provider = YahooProvider()
        self.universe_manager = UniverseManager()
        self.scanner_service = ScannerService(
            provider=self.provider,
            universe_manager=self.universe_manager,
            max_workers=8,
        )

        self.portfolio_store = PortfolioStore()
        self.trade_history_store = TradeHistoryStore()
        self.trade_manager = TradeManager(
            portfolio_store=self.portfolio_store,
            trade_history_store=self.trade_history_store,
        )

        self.portfolio = self.portfolio_store.load()
        self.active_universe = "swing"

        self.workspace_controller = WorkspaceController()
        self.pages = QStackedWidget()
        self.workspace_page_indexes = {
            GuiPage.DASHBOARD: 0,
            GuiPage.SCANNER: 1,
            GuiPage.PORTFOLIO: 2,
            GuiPage.HISTORY: 3,
            GuiPage.SETTINGS: 4,
        }

        self.dashboard_page = DashboardWorkspace(
            theme=self.theme,
            on_scan_requested=self.scan_market,
        )
        self.scanner_page = ScannerWorkspace(theme=self.theme)
        self.portfolio_page = PortfolioWorkspace(theme=self.theme)
        self.history_page = HistoryWorkspace(theme=self.theme)
        self.settings_page = SettingsWorkspace(theme=self.theme)
        self.settings_page.set_settings(self.format_settings())

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.scanner_page)
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
        sidebar.setFixedWidth(self.theme.metrics.sidebar_width)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("ORION")
        title.setStyleSheet(self.theme.title_style() + "; margin: 20px;")

        subtitle = QLabel("AI Swing Trader")
        subtitle.setStyleSheet(
            self.theme.muted_text_style()
            + "; margin-left: 20px; margin-bottom: 30px;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        buttons = [
            ("Dashboard", GuiPage.DASHBOARD),
            ("Scanner", GuiPage.SCANNER),
            ("Portfolio", GuiPage.PORTFOLIO),
            ("Historie", GuiPage.HISTORY),
            ("Instellingen", GuiPage.SETTINGS),
        ]

        for text, page in buttons:
            button = QPushButton(text)
            button.clicked.connect(
                lambda checked=False, target_page=page: self.navigate_to_workspace(
                    target_page
                )
            )
            button.setStyleSheet(self.sidebar_button_style())
            layout.addWidget(button)

        sidebar.setLayout(layout)
        sidebar.setObjectName("OrionSidebar")
        return sidebar

    def navigate_to_workspace(self, page: GuiPage):
        result = self.workspace_controller.navigate_to(page)
        page_index = self.workspace_page_indexes[result.state.current_page]
        self.pages.setCurrentIndex(page_index)


    

    def scan_market(self):
        try:
            self.dashboard_page.set_status_text("Orion analyseert de markt...")
            self.scanner_page.set_status_text("Scanner analyseert de markt...")
            self.scanner_page.set_summary_html("Resultaten worden opgehaald...")
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

            self.dashboard_page.set_advice_html(
                self.format_advice(
                    trade_plans=trade_plans,
                    managed_trades=managed_trades,
                )
            )
            self.scanner_page.set_status_text("Scanneranalyse voltooid.")
            self.scanner_page.set_summary_html(
                self.format_advice(
                    trade_plans=trade_plans,
                    managed_trades=managed_trades,
                )
            )
            self.portfolio_page.set_overview(self.format_portfolio())
            self.history_page.set_history(self.format_trade_history())

        except Exception as error:
            self.dashboard_page.set_status_text(f"Fout tijdens scan: {error}")
            self.scanner_page.set_status_text("Scanneranalyse mislukt.")
            self.scanner_page.set_summary_html(f"Fout tijdens scan: {error}")
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

    def format_trade_history(self):
        trades = self.trade_history_store.load()

        if not trades:
            return """
            <div style="background:#1f2937; border-radius:16px; padding:24px;">
                <h2>Geen historie</h2>
                <p>Er zijn nog geen trade-events opgeslagen.</p>
            </div>
            """

        html = """
        <div style="background:#1f2937; border-radius:16px; padding:24px;">
            <h2>Trade history</h2>
        """

        for trade in reversed(trades[-20:]):
            action = trade.get("action", "UNKNOWN")
            symbol = trade.get("symbol", "")
            quantity = trade.get("quantity", 0)
            price = float(trade.get("price", 0.0))
            timestamp = trade.get("timestamp", "")
            reason = trade.get("reason", "")

            color = "#9ca3af"
            if action == "BUY":
                color = "#22c55e"
            elif action == "SELL":
                color = "#f97316"
            elif action == "HOLD":
                color = "#3b82f6"

            html += f"""
            <div style="background:#111827; border-left:5px solid {color}; border-radius:12px; padding:16px; margin:12px 0;">
                <h3 style="color:{color};">{action} {symbol}</h3>
                <p><b>Aantal:</b> {quantity}</p>
                <p><b>Prijs:</b> {price:.2f}</p>
                <p><b>Tijd:</b> {timestamp}</p>
                <p>{reason}</p>
            </div>
            """

        html += "</div>"
        return html

    def format_settings(self):
        universe = self.universe_manager.get_universe(self.active_universe)

        return f"""
        <div style="background:#1f2937; border-radius:16px; padding:24px;">
            <h2>Actieve instellingen</h2>
            <p><b>Universe:</b> {universe.name}</p>
            <p><b>Aantal symbols:</b> {len(self.universe_manager.get_symbols(self.active_universe))}</p>
            <p><b>Max positiegrootte:</b> {self.portfolio.max_position_percentage * 100:.0f}% van cash</p>
            <p><b>Handelsstijl:</b> Swing trades van enkele uren tot enkele dagen.</p>
        </div>
        """

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