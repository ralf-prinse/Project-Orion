import sys

from PySide6.QtWidgets import QApplication

from ui.design import ORION_DARK_THEME
from ui.foundation.desktop_bootstrap import DesktopBootstrap
from ui.workspace.trading_dashboard_workspace import TradingDashboardWorkspace


def get_or_create_app():
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    return app


def test_desktop_bootstrap_creates_dashboard_workspace():
    get_or_create_app()

    bootstrap = DesktopBootstrap(theme=ORION_DARK_THEME)

    dashboard = bootstrap.create_dashboard()

    assert isinstance(dashboard, TradingDashboardWorkspace)
    assert bootstrap.services.trading_dashboard_controller is not None


def main():
    print("\n=========================================")
    print("ORION DESKTOP BOOTSTRAP TEST")
    print("=========================================\n")

    test_desktop_bootstrap_creates_dashboard_workspace()

    print("DESKTOP BOOTSTRAP: PASS ✅")


if __name__ == "__main__":
    main()