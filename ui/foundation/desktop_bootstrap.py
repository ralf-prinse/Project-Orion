from __future__ import annotations

"""
DesktopBootstrap

Composition Root van Project Orion.

Alle objecten die nodig zijn om de desktop op te bouwen
worden hier geconfigureerd.

Businesslogica hoort hier NIET thuis.

Taken:

- repositories aanmaken
- services aanmaken
- controllers aanmaken
- workspaces koppelen
- timers registreren
- dependency wiring
"""

from dataclasses import dataclass

from ui.foundation.trading_dashboard_controller import (
    TradingDashboardController,
)
from ui.workspace.trading_dashboard_workspace import (
    TradingDashboardWorkspace,
)


@dataclass(slots=True)
class DesktopServices:
    """
    Centrale container voor gedeelde services.
    """

    trading_dashboard_controller: TradingDashboardController


class DesktopBootstrap:
    """
    Centrale Composition Root.

    In volgende sprints zal deze klasse verantwoordelijk zijn voor:

    - Dashboard
    - Mission Control
    - Position Monitor
    - Trading
    - Settings

    Uiteindelijk vervangt deze bootstrap de huidige
    initialisatie uit main_window.py.
    """

    def __init__(self, theme):
        self.theme = theme

    def create_dashboard(self) -> TradingDashboardWorkspace:
        workspace = TradingDashboardWorkspace(
            theme=self.theme,
        )

        controller = TradingDashboardController(
            workspace=workspace,
        )

        controller.refresh()

        self.services = DesktopServices(
            trading_dashboard_controller=controller,
        )

        return workspace