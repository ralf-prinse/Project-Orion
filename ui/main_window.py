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

from ui.foundation.history_presenter import HistoryPresenter
from ui.foundation.settings_presenter import SettingsPresenter
from ui.foundation.trade_advice_presenter import TradeAdvicePresenter
from ui.foundation.workspace_coordinator import WorkspaceCoordinator

from ui.workspace.dashboard_workspace import DashboardWorkspace
from ui.workspace.history_workspace import HistoryWorkspace
from ui.workspace.portfolio_workspace import PortfolioWorkspace
from ui.workspace.scanner_workspace import ScannerWorkspace
from ui.workspace.settings_workspace import SettingsWorkspace
from ui.workspace.performance_workspace import PerformanceWorkspace

from ui.workspace.workspace_controller import WorkspaceController


class OrionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # -------------------------
        # THEME
        # -------------------------
        self.theme = ORION_DARK_THEME

        self.setWindowTitle("Project Orion")
        self.resize(
            self.theme.metrics.default_window_width,
            self.theme.metrics.default_window_height,
        )

        # -------------------------
        # DATA / SERVICES
        # -------------------------
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

        # -------------------------
        # PRESENTERS
        # -------------------------
        self.history_presenter = HistoryPresenter()
        self.settings_presenter = SettingsPresenter()
        self.trade_advice_presenter = TradeAdvicePresenter()

        # -------------------------
        # COORDINATOR
        # -------------------------
        self.workspace_coordinator = WorkspaceCoordinator()
        self.workspace_controller = WorkspaceController()

        # -------------------------
        # PAGES (UI WORKSPACES)
        # -------------------------
        self.pages = QStackedWidget()

        self.workspace_page_indexes = {
            "dashboard": 0,
            "scanner": 1,
            "portfolio": 2,
            "performance": 3,   # ✅ FIXED
            "history": 4,
            "settings": 5,
        }

        # -------------------------
        # WORKSPACES
        # -------------------------
        self.dashboard_page = DashboardWorkspace(
            theme=self.theme,
            on_scan_requested=self.scan_market,
        )

        self.scanner_page = ScannerWorkspace(theme=self.theme)
        self.portfolio_page = PortfolioWorkspace(theme=self.theme)

        # ✅ PERFORMANCE PAGE (FIXED ORDER)
        self.performance_page = PerformanceWorkspace(theme=self.theme)

        self.history_page = HistoryWorkspace(theme=self.theme)
        self.settings_page = SettingsWorkspace(theme=self.theme)

        # -------------------------
        # INIT WORKSPACES
        # -------------------------
        self._initialize_settings_workspace()
        self._initialize_portfolio_workspace()

        # IMPORTANT: must come AFTER all pages exist
        self._initialize_pages()

    # -------------------------
    # SETTINGS
    # -------------------------
    def _initialize_settings_workspace(self):
        universe = self.universe_manager.get_universe(self.active_universe)

        self.settings_page.set_sections(
            self.settings_presenter.create_sections(
                universe_name=universe.name,
                symbol_count=len(
                    self.universe_manager.get_symbols(self.active_universe)
                ),
                max_position_percentage=self.portfolio.max_position_percentage,
            )
        )

    # -------------------------
    # PORTFOLIO
    # -------------------------
    def _initialize_portfolio_workspace(self):
        portfolio_workspace = self.workspace_coordinator.create_portfolio_workspace(
            self.portfolio
        )

        self.portfolio_page.set_workspace(portfolio_workspace)

    # -------------------------
    # PAGE SETUP
    # -------------------------
    def _initialize_pages(self):
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.scanner_page)
        self.pages.addWidget(self.portfolio_page)
        self.pages.addWidget(self.performance_page)   # ✅ FIXED
        self.pages.addWidget(self.history_page)
        self.pages.addWidget(self.settings_page)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_sidebar())
        main_layout.addWidget(self.pages, stretch=1)

        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet(self.stylesheet())

        self.setCentralWidget(container)

    # -------------------------
    # SIDEBAR
    # -------------------------
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
            ("Dashboard", "dashboard"),
            ("Scanner", "scanner"),
            ("Portfolio", "portfolio"),
            ("Performance", "performance"),  # ✅ FIXED
            ("Historie", "history"),
            ("Instellingen", "settings"),
        ]

        for text, page in buttons:
            button = QPushButton(text)
            button.clicked.connect(
                lambda checked=False, target_page=page: self.navigate_to_workspace(
                    target_page
                )
            )
            layout.addWidget(button)

        sidebar.setLayout(layout)
        return sidebar

    # -------------------------
    # NAVIGATION
    # -------------------------
    def navigate_to_workspace(self, page: str):
        index = self.workspace_page_indexes[page]
        self.pages.setCurrentIndex(index)

    # -------------------------
    # SCAN
    # -------------------------
    def scan_market(self):
        try:
            self.dashboard_page.set_status_text("Orion analyseert de markt...")
            self.scanner_page.set_status_text("Scanner analyseert de markt...")

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

            trade_advice_sections = self.trade_advice_presenter.create_sections(
                trade_plans=trade_plans,
                managed_trades=managed_trades,
            )

            self.dashboard_page.set_sections(trade_advice_sections)
            self.scanner_page.set_sections(trade_advice_sections)

            self._initialize_portfolio_workspace()

            trades = self.trade_history_store.load()
            self.history_page.set_sections(
                self.history_presenter.create_sections(trades)
            )

        except Exception as error:
            self.dashboard_page.set_status_text(f"Fout: {error}")
            self.scanner_page.set_status_text("Scanner mislukt.")

    # -------------------------
    # STYLE
    # -------------------------
    def stylesheet(self):
        return """
        QWidget {
            background-color: #111827;
            color: #f9fafb;
            font-family: Arial;
        }
        """
