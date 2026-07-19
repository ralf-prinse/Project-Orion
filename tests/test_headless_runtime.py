from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_desktop_gui_and_qt_dependency_are_removed():
    assert not (ROOT / "app.py").exists()
    assert not (ROOT / "ui").exists()
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert "PySide6" not in requirements


def test_cli_dashboard_remains_available():
    from presentation.trading_dashboard_cli_presenter import (
        TradingDashboardCliPresenter,
    )

    assert TradingDashboardCliPresenter is not None
