from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from ui.foundation.workspace import GuiWorkspace
from ui.foundation.workspace_renderer import WorkspaceRenderer
from ui.workspace.base_workspace import BaseWorkspace
from ui.workspace.chart_container import ChartContainer
from ui.workspace.dashboard_grid import DashboardGrid


class MissionControlWorkspace(BaseWorkspace):
    """
    Primary Mission Control workspace.

    Presentation only.

    Mission Control renders GuiWorkspace models through the canonical
    WorkspaceRenderer pipeline.

    Responsibilities:
        - own the Mission Control layout
        - expose a scan trigger button
        - mount dashboard and chart containers
        - render prepared GuiWorkspace presentation models
        - forward selected opportunity symbols to the application shell

    No business logic.
    No trading calculations.
    No scanner orchestration.
    No AI logic.
    """

    opportunity_selected = Signal(str)

    def __init__(
        self,
        theme,
        on_scan_requested: Callable[[], None] | None = None,
    ):
        super().__init__(
            theme=theme,
            title="Mission Control",
            intro=(
                "Centrale Orion-workspace voor marktstatus, live scanner, "
                "top opportunities en trading-overzicht."
            ),
        )

        self._on_scan_requested = on_scan_requested

        self.scan_button = QPushButton("Scan markt")
        self.scan_button.setStyleSheet(self.primary_button_style())
        self.scan_button.clicked.connect(self._handle_scan_requested)

        self.dashboard_grid = DashboardGrid(theme=self.theme)
        self.dashboard_grid.opportunity_selected.connect(
            self._handle_opportunity_selected
        )

        self.chart_container = ChartContainer()

        self.workspace_renderer = WorkspaceRenderer(
            dashboard_grid=self.dashboard_grid,
            chart_container=self.chart_container,
        )

        self._build_layout()
        self.set_workspace(self._create_empty_workspace())

    def _build_layout(self) -> None:
        self.add_workspace_widget(self.scan_button)
        self.add_workspace_widget(self.dashboard_grid)
        self.add_workspace_widget(self.chart_container)

    def set_workspace(self, workspace: GuiWorkspace) -> None:
        """
        Render a complete Mission Control workspace.

        The workspace data must already be prepared by presenters or services.
        """

        self.workspace_renderer.render(workspace)

    def set_status_text(self, text: str) -> None:
        """
        Backward-compatible status adapter.

        Keeps Mission Control presentation-only while allowing callers to show
        a simple status message before dedicated presenters are connected.
        """

        self.set_workspace(
            GuiWorkspace(
                title="Mission Control",
                subtitle="Status",
                panels=[
                    self._status_panel(text),
                ],
                metadata={},
            )
        )

    def _handle_scan_requested(self) -> None:
        if self._on_scan_requested is not None:
            self._on_scan_requested()

    def _handle_opportunity_selected(self, symbol: str) -> None:
        cleaned_symbol = str(symbol).strip().upper()

        if not cleaned_symbol:
            return

        self.opportunity_selected.emit(cleaned_symbol)

    def _create_empty_workspace(self) -> GuiWorkspace:
        return GuiWorkspace(
            title="Mission Control",
            subtitle="Wacht op live scanner-data.",
            panels=[
                self._status_panel("Mission Control gereed."),
                self._market_status_panel(),
                self._top_opportunities_panel(),
            ],
            metadata={},
        )

    def _status_panel(self, text: str):
        from ui.foundation.workspace import GuiWorkspacePanel

        return GuiWorkspacePanel(
            panel_type="mission_control_status",
            title="Status",
            subtitle=text,
            items=[],
            status="info",
            metadata={},
        )

    def _market_status_panel(self):
        from ui.foundation.workspace import GuiWorkspacePanel

        return GuiWorkspacePanel(
            panel_type="market_status",
            title="Market Status",
            subtitle="Nog geen marktsnapshot beschikbaar.",
            items=[],
            status="neutral",
            metadata={},
        )

    def _top_opportunities_panel(self):
        from ui.foundation.workspace import GuiWorkspacePanel

        return GuiWorkspacePanel(
            panel_type="top_opportunities",
            title="Top Opportunities",
            subtitle="Nog geen opportunities beschikbaar.",
            items=[],
            status="neutral",
            metadata={},
        )

    def primary_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            padding: 15px 18px;
            border-radius: 14px;
            margin-bottom: 22px;
            border: 1px solid #3b82f6;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
            border: 1px solid #60a5fa;
        }

        QPushButton:pressed {
            background-color: #1e40af;
        }
        """