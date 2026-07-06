from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from services.portfolio_store import PortfolioStore
from services.trade_history_store import TradeHistoryStore
from services.universe_manager import UniverseManager

from ui.design import ORION_DARK_THEME
from datetime import datetime

from models.trade_lifecycle import ExitSignal, Trade, TradeStatus
from services.open_trade_store import OpenTradeStore
from services.trade_lifecycle_service import TradeLifecycleService
from ui.foundation.history_presenter import HistoryPresenter
from ui.foundation.mission_control_controller import MissionControlController
from ui.foundation.position_monitor_controller import PositionMonitorController
from ui.foundation.settings_presenter import SettingsPresenter
from ui.foundation.trading_controller import TradingController
from ui.foundation.workspace_coordinator import WorkspaceCoordinator

from ui.workspace.history_workspace import HistoryWorkspace
from ui.workspace.mission_control_workspace import MissionControlWorkspace
from ui.workspace.performance_workspace import PerformanceWorkspace
from ui.workspace.portfolio_workspace import PortfolioWorkspace
from ui.workspace.position_monitor_workspace import PositionMonitorWorkspace
from ui.workspace.scanner_workspace import ScannerWorkspace
from ui.workspace.settings_workspace import SettingsWorkspace
from ui.workspace.trading_workspace import TradingWorkspace
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

        self.universe_manager = UniverseManager()

        self.portfolio_store = PortfolioStore()
        self.trade_history_store = TradeHistoryStore()
        self.open_trade_store = OpenTradeStore()
        self.trade_lifecycle_service = TradeLifecycleService(
    open_trade_store=self.open_trade_store,
    trade_history_store=self.trade_history_store,
)
        self.portfolio = self.portfolio_store.load()
        self.active_universe = "swing"

        self.history_presenter = HistoryPresenter()
        self.settings_presenter = SettingsPresenter()

        self.workspace_coordinator = WorkspaceCoordinator()
        self.workspace_controller = WorkspaceController()

        self.pages = QStackedWidget()

        self.workspace_page_indexes = {
            "mission_control": 0,
            "scanner": 1,
            "trading": 2,
            "position_monitor": 3,
            "portfolio": 4,
            "performance": 5,
            "history": 6,
            "settings": 7,
        }

        # ----------------------------
        # WORKSPACES
        # ----------------------------

        self.mission_control_page = MissionControlWorkspace(
            theme=self.theme,
            on_scan_requested=self.scan_market,
        )
        self.mission_control_page.opportunity_selected.connect(
            self._handle_mission_control_opportunity_selected
        )

        self.scanner_page = ScannerWorkspace(theme=self.theme)

        self.trading_page = TradingWorkspace(
            theme=self.theme,
            on_analyze_requested=self.analyze_symbol,
            on_open_trade_requested=self.open_trade_from_last_analysis,
        )

        self.position_monitor_page = PositionMonitorWorkspace(
            theme=self.theme,
            on_monitor_requested=self.monitor_trade,
        )

        self.portfolio_page = PortfolioWorkspace(
            theme=self.theme,
            initial_cash=self.portfolio.cash,
            currency=self.portfolio.currency,
        )
        self.portfolio_page.capital_saved.connect(
            self._handle_capital_saved
        )

        self.performance_page = PerformanceWorkspace(theme=self.theme)
        self.history_page = HistoryWorkspace(theme=self.theme)
        self.settings_page = SettingsWorkspace(theme=self.theme)

        # ----------------------------
        # CONTROLLERS
        # ----------------------------

        self.mission_control_controller = MissionControlController(
            workspace=self.mission_control_page,
            available_cash_provider=lambda: self.portfolio.cash,
        )

        self.mission_refresh_timer = QTimer(self)
        self.mission_refresh_timer.setInterval(60_000)
        self.mission_refresh_timer.timeout.connect(
            self.mission_control_controller.refresh
        )

        self.trading_controller = TradingController(
            trading_workspace=self.trading_page,
            portfolio_state=self.portfolio,
        )

        self.position_monitor_controller = PositionMonitorController(
            workspace=self.position_monitor_page,
        )

        self.position_monitor_controller.load_open_trades()

        # ----------------------------
        # INIT WORKSPACES
        # ----------------------------

        self._initialize_settings_workspace()
        self._initialize_portfolio_workspace()
        self._initialize_history_workspace()
        self._initialize_pages()

        self.mission_control_controller.initialize()
        self.mission_refresh_timer.start()

    # ----------------------------
    # INIT METHODS
    # ----------------------------

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

    def _initialize_portfolio_workspace(self):
        portfolio_workspace = self.workspace_coordinator.create_portfolio_workspace(
            self.portfolio
        )

        self.portfolio_page.set_workspace(portfolio_workspace)

    def _initialize_history_workspace(self):
        trades = self.trade_history_store.load()

        self.history_page.set_sections(
            self.history_presenter.create_sections(trades)
        )

    # ----------------------------
    # UI SETUP
    # ----------------------------

    def _initialize_pages(self):
        self.pages.addWidget(self.mission_control_page)
        self.pages.addWidget(self.scanner_page)
        self.pages.addWidget(self.trading_page)
        self.pages.addWidget(self.position_monitor_page)
        self.pages.addWidget(self.portfolio_page)
        self.pages.addWidget(self.performance_page)
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
            ("Mission Control", "mission_control"),
            ("Scanner", "scanner"),
            ("Trading", "trading"),
            ("Trade Monitor", "position_monitor"),
            ("Portfolio", "portfolio"),
            ("Performance", "performance"),
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

    # ----------------------------
    # NAVIGATION
    # ----------------------------

    def navigate_to_workspace(self, page: str):
        index = self.workspace_page_indexes[page]
        self.pages.setCurrentIndex(index)

    # ----------------------------
    # ACTIONS
    # ----------------------------

    def analyze_symbol(self, symbol: str):
        self.trading_controller.analyze_symbol(symbol)

    def open_trade_from_last_analysis(self):
        self.trading_page.set_status_text(
        "Open Trade workflow wordt gekoppeld..."
    )

    def monitor_trade(self, trade):
        self.position_monitor_controller.monitor_trade(trade)

    def _handle_capital_saved(self, amount: float):
        """
        Save the available trading capital.

        MainWindow owns the PortfolioStore and is therefore responsible
        for persistence.
        """

        self.portfolio.cash = float(amount)
        self.portfolio_store.save(self.portfolio)

    def scan_market(self):
        self.mission_control_controller.refresh()

    def _handle_mission_control_opportunity_selected(self, symbol: str):
        normalized_symbol = str(symbol).strip().upper()

        if not normalized_symbol:
            return

        self.navigate_to_workspace("trading")
        self.trading_page.set_symbol(normalized_symbol)
        self.trading_page.analyze_current_symbol()

    # ----------------------------
    # STYLES
    # ----------------------------

    def stylesheet(self):
        return """
        QWidget {
            background-color: #111827;
            color: #f9fafb;
            font-family: Arial;
        }
        """